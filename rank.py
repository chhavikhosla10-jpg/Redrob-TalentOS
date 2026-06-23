import argparse, csv, json, heapq
from datetime import datetime, date

POS_SKILLS = {
    'embeddings':4.0,'sentence transformers':4.0,'semantic search':4.0,'vector search':4.0,
    'information retrieval':4.0,'recommendation systems':4.0,'ranking':3.8,'search':3.0,
    'rag':2.5,'llms':2.0,'fine-tuning llms':2.2,'lora':1.4,'qlora':1.5,'peft':1.5,
    'nlp':2.2,'python':2.5,'fastapi':1.0,'faiss':3.0,'pinecone':2.6,'qdrant':2.6,
    'weaviate':2.6,'milvus':2.6,'opensearch':2.1,'elasticsearch':2.4,'xgboost':1.8,
    'learning to rank':2.5,'ab testing':1.8,'experimentation':1.5,'ndcg':2.2,'mrr':1.8,
    'map':1.6,'pytorch':1.3,'tensorflow':1.0,'hugging face transformers':1.5,
    'transformers':1.3,'kubernetes':0.5,'docker':0.4,'distributed systems':1.5,
    'large scale inference':1.4,'model deployment':1.5
}
NEG_SKILLS = {'photoshop':-1,'salesforce crm':-1,'accounting':-1,'tally':-1,'sales':-1,'marketing':-1,'content writing':-1,'seo':-0.8,'figma':-0.8,'illustrator':-0.8,'yolo':-0.7,'speech recognition':-0.6,'tts':-0.5,'image classification':-0.6,'gans':-0.4}
TITLE_GOOD = ['search engineer','recommendation systems engineer','applied ml engineer','machine learning engineer','ml engineer','ai engineer','senior software engineer (ml)','senior data scientist','data scientist','ai specialist','ai research engineer']
TITLE_OK = ['data engineer','senior data engineer','backend engineer','software engineer','senior software engineer','analytics engineer','cloud engineer','full stack developer']
BAD_TITLE = ['marketing','hr','sales','accountant','graphic','mechanical','civil','customer support','operations manager','content writer','project manager','business analyst']
PRODUCT_INDUSTRIES = ['Software','Fintech','Food Delivery','E-commerce','EdTech','SaaS','AI/ML','AdTech','Transportation','Insurance Tech','Gaming','HealthTech','HealthTech AI','Conversational AI','Voice AI','Internet']
CONSULT = ['tcs','infosys','wipro','accenture','cognizant','capgemini','mindtree']
TIER1_INDIA = ['Noida','Pune','Delhi','Gurgaon','Bangalore','Hyderabad','Mumbai','Chennai']

def clamp(x,a,b): return max(a,min(b,x))

def recency_score(d):
    try:
        days = (date(2026,6,1) - datetime.strptime(d,'%Y-%m-%d').date()).days
        return max(0, 1 - max(days,0)/180)
    except Exception:
        return 0.3

def score_candidate(c):
    p, sig = c['profile'], c['redrob_signals']
    text = ' '.join([p.get('headline',''), p.get('summary',''), p.get('current_title',''), p.get('current_industry','')] + [h.get('title','')+' '+h.get('industry','')+' '+h.get('description','') for h in c.get('career_history',[])])
    low, title = text.lower(), p.get('current_title','').lower()
    score = 0.0
    y = float(p.get('years_of_experience') or 0)
    score += 16 - abs(7-y)*1.5 if 5 <= y <= 9 else (8 if 4 <= y < 5 or 9 < y <= 11 else -6)
    if any(t in title for t in TITLE_GOOD): score += 18
    elif any(t in title for t in TITLE_OK): score += 8
    if any(t in title for t in BAD_TITLE): score -= 22
    if p.get('current_industry') in PRODUCT_INDUSTRIES: score += 9
    elif p.get('current_industry') in ['IT Services','Consulting']: score -= 8
    companies = [h.get('company','').lower() for h in c.get('career_history',[])]
    if companies and all(any(co == x or x in co for x in CONSULT) for co in companies): score -= 10
    elif any(h.get('industry') in PRODUCT_INDUSTRIES for h in c.get('career_history',[])): score += 6
    skill_score, core_count, impossible = 0, 0, 0
    for s in c.get('skills',[]):
        nm, prof = s.get('name','').lower().strip(), s.get('proficiency','')
        dur = s.get('duration_months') or 0
        if prof == 'expert' and dur < 6: impossible += 1
        mult = {'beginner':0.35,'intermediate':0.65,'advanced':0.9,'expert':1.1}.get(prof,0.5)
        dur_mult = clamp(dur/36,0.2,1.2)
        if nm in POS_SKILLS:
            skill_score += POS_SKILLS[nm] * mult * dur_mult
            if POS_SKILLS[nm] >= 2.5: core_count += 1
        if nm in NEG_SKILLS: skill_score += NEG_SKILLS[nm]
    score += min(skill_score,38) + (8 if core_count >= 5 else 4 if core_count >= 3 else 0)
    for ph,w in {'production':2.5,'deployed':2.5,'shipped':2.5,'real users':2.5,'at scale':2,'embedding drift':4,'index refresh':3,'retrieval-quality regression':4,'hybrid retrieval':4,'ranking system':4,'search ranking':4,'recommendation system':4,'recommender':3,'vector database':3,'faiss':2.5,'pinecone':2,'qdrant':2,'weaviate':2,'milvus':2,'elasticsearch':2,'opensearch':2,'ndcg':3,'mrr':2.5,'map':2.5,'a/b testing':3,'offline benchmark':2.5,'evaluation framework':3,'recruiter':1.5,'marketplace':1.2,'hr-tech':2,'talent':1.5}.items():
        if ph in low: score += w
    if ('computer vision' in low or 'speech' in low or 'robotics' in low) and not any(k in low for k in ['retrieval','ranking','search','recommendation','nlp']): score -= 8
    if 'langchain' in low and not any(k in low for k in ['production','retrieval','ranking','search','recommendation','vector']): score -= 5
    loc = p.get('location','')
    score += 7 if any(city in loc for city in ['Noida','Pune']) else 4 if any(city in loc for city in TIER1_INDIA) else 1 if p.get('country')=='India' else -7
    if sig.get('willing_to_relocate'): score += 3
    score += clamp((sig.get('profile_completeness_score',0)-50)/50*3,-2,3)
    score += 5 if sig.get('open_to_work_flag') else -2
    score += clamp(sig.get('recruiter_response_rate',0)*8,0,8)
    score += 3 if sig.get('avg_response_time_hours',72) <= 12 else (1.5 if sig.get('avg_response_time_hours',72) <= 36 else -2)
    score += recency_score(sig.get('last_active_date',''))*6
    score += clamp(sig.get('profile_views_received_30d',0)/20,0,3) + clamp(sig.get('saved_by_recruiters_30d',0)/5,0,3)
    score += clamp(sig.get('github_activity_score',-1)/100*4,-1,4) + clamp(sig.get('interview_completion_rate',0)*4,0,4)
    if sig.get('offer_acceptance_rate',-1) >= 0: score += sig.get('offer_acceptance_rate',0)*2
    notice = sig.get('notice_period_days',90)
    score += 5 if notice <= 30 else 1 if notice <= 60 else -4
    if sig.get('verified_email'): score += 0.8
    if sig.get('verified_phone'): score += 0.8
    if sig.get('linkedin_connected'): score += 0.8
    for key,val in (sig.get('skill_assessment_scores') or {}).items():
        if key.lower() in POS_SKILLS: score += clamp((val-60)/40*2,0,2)
    if impossible >= 3: score -= 30
    return score

def reasoning(c):
    p, sig = c['profile'], c['redrob_signals']
    skills = [x['name'] for x in c.get('skills',[]) if x['name'].lower() in POS_SKILLS]
    top = ', '.join(skills[:5]) if skills else 'applied ML/search-adjacent skills'
    concerns = []
    if sig.get('notice_period_days',0) > 60: concerns.append(f"notice period is {sig.get('notice_period_days')} days")
    if sig.get('recruiter_response_rate',0) < 0.35: concerns.append(f"response rate is {sig.get('recruiter_response_rate'):.2f}")
    if p.get('current_industry') in ['IT Services','Consulting']: concerns.append('service-company background')
    end = ' Concern: ' + ', '.join(concerns[:2]) + '.' if concerns else ' Strong recent availability signals and hiring responsiveness.'
    return f"{p.get('current_title')} with {p.get('years_of_experience')} yrs in {p.get('current_industry')}; matches the JD through {top} and {p.get('location')} / relocation fit.{end}"

def rank(candidates_path, out_path):
    heap=[]
    with open(candidates_path, encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            c=json.loads(line)
            s=score_candidate(c)
            item=(s,c['candidate_id'],c)
            if len(heap)<500: heapq.heappush(heap,item)
            elif item[0]>heap[0][0]: heapq.heapreplace(heap,item)
    best=sorted(heap, key=lambda x:(-x[0],x[1]))[:100]
    with open(out_path,'w',encoding='utf-8',newline='') as fp:
        wr=csv.writer(fp)
        wr.writerow(['candidate_id','rank','score','reasoning'])
        for rank,(s,cid,c) in enumerate(best,1):
            wr.writerow([cid,rank,f'{0.9900-(rank-1)*0.0025:.4f}',reasoning(c)])

if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--candidates', required=True)
    ap.add_argument('--out', required=True)
    args=ap.parse_args()
    rank(args.candidates, args.out)

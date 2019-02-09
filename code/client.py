import praw
import numpy as np
from matplotlib import pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sqlite3
import sys
import codecs
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Auth
reddit = praw.Reddit(client_id='GKG50iWjxkkcew',
                     client_secret="6OKCI0V-OzGp5kx-fs7HN2QA_vM",
                     password='10488724593163d6045e1f53b56543f7',
                     user_agent='USERAGENT',
                     username='throwaway2244561')




############ Creates objects for emoji tokenizing ###########
# emoticons_str = r"""
#     (?:
#         [:=;] # Eyes
#         [oO\-]? # Nose (optional)
#         [D\)\]\(\]/\\OpP] # Mouth
#     )"""
# regex_str = [
#     emoticons_str,
#     r'<[^>]+>', # HTML tags
#     r'(?:@[\w_]+)', # @-mentions
#     r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
#     r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
#     r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
#     r'(?:[\w_]+)', # other words
#     r'(?:\S)' # anything else
# ]
# tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
# emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)


acroynms = {
'ACC': 'Air Combat Command',
'ACDA': 'United States Arms Control and Disarmament Agency',
'ACF': 'Administration for Children and Families',
'ACFR': 'Administrative Committee of the Federal Register',
'ACHP': 'Advisory Council on Historic Preservation',
'ACQWeb': 'Office of the Under Secretary of Defense for Acquisition and Technology',
'ACS': 'Office of American Citizens Services and Crisis Management',
'ACSFA': 'Advisory Committee on Student Financial Assistance',
'ACYF': 'Administration for Children, Youth, and Families',
'BATF': 'Bureau of Alcohol, Tobacco & Firearms',
'BEA': 'Bureau of Economic Affairs',
'BLS': 'Bureau of Labor Statistics',
'BNL': 'Brookhaven National Laboratory',
'BOP': 'Federal Bureau of Prisons',
'BOR': 'Bureau of Reclamation',
'BPA': 'Bonneville Power Administration',
'BPC': 'Best Practices Committee',
'BPD': 'Bureau of the Public Debt',
'BPHC': 'Bureau of Primary Health Care',
'BRAC': 'Defense Base Closure and Realignment Commission',
'BRB': 'Benefits Review Board',
'BRD': 'Biological Resource Division',
'BTA': 'Business Transformation Agency',
'BTOP': 'Broadband Technology Opportunities Program',
'CAOC': 'Chief Acquisition Officers Council',
'CAP': 'Civil Air Patrol',
'CASMIRC': 'Child Abduction and Serial Murder Investigative Resources Center',
'CATC': 'Clean Air Technology Center',
'CBCA': 'Civilian Board of Contract Appeals',
'CPS': 'Center for Policy Studies',
'CSRS': 'Civil Service Retirement System',
'DERT': 'Division of Extramural Research & Training',
'DESA': 'Department of Economic and Social Affairs',
'DESC': 'Defense Energy Support Center',
'DFAS': 'Defense Finance and Accounting Service',
'DFEC': 'Division of Federal Employees Compensation',
'DHAC': 'Division of Health Assessment and Consultation',
'DHS': 'Department of Homeland Security',
'DOE': 'Department of Energy',
'DOI': 'Department of Interior',
'DOJ': 'Department of Justice',
'DOL': 'Department of Labor',
'EEOC': 'Equal Employment Opportunity Commission',
'EEOICP': 'Energy Employees Occupational Illness Compensation Program',
'EEOMBD': 'Ombudsman for the Energy Employees Occupational Illness Compensation Program',
'FBI': 'Federal Bureau of Investigation',
'FDA': 'Food and Drug Administration',
'FDIC': 'Federal Deposit Insurance Corporation',
'FEC': 'Federal Election Commission',
'FEMA': 'Federal Emergency Management Agency',
'FJC': 'Federal Judicial Center',
'FLC': 'Federal Laboratory Consortium',
'FLETC': 'Federal Law Enforcement Training Center',
'FLH': 'Office of Federal Lands Highway',
'FLICC': 'Federal Library and Information Center Committee',
'FLRA': 'Federal Labor Relations Authority',
'FMC': 'Federal Maritime Commission',
'FOIA': 'Freedom of Information Act',
'GPC': 'Grants Policy Committee',
'GPO': 'Government Printing Office',
'GPRA': 'Government Performance and Results Act',
'GSA': 'General Services Administration',
'GSFC': 'Goddard Space Flight Center',
'GSTC': 'Geospatial Service and Technology Center',
'G/TIP': 'Office to Monitor and Combat Trafficking in Persons',
'HIP': 'Migratory Bird Harvest Information Program',
'HIPAA': 'Health Insurance Portability and Accountability Act of 1996',
'HISPC': 'Health Information Security and Privacy Collaboration',
'HMDA': 'Home Mortgage Disclosure Act',
'HMI': 'Healthy Marriage Initiative',
'HPCC': 'High Performance Computing and Communications',
'LM': 'Office of Legacy Management',
'LOC': 'Library of Congress',
'LOCIS': 'Library of Congress Information System',
'LSC': 'Legal Services Corporation',
'MDA': 'Missile Defense Agency',
'MDB': 'Multilateral Development Banks',
'MedPAC': 'Medicare Payment Advisory Commission',
'MEP': 'Manufacturing Extension Partnership',
'M&M': 'Medicare and Medicaid',
'OACU': 'Office of Animal Care and Use',
'OAG': 'Office of the Attorney General',
'OAHP': 'Office of Affordable Housing Preservation',
'OAIT': 'Office of American Indian Trust',
'OALJ': 'Office of Administrative Law Judges',
'PO': 'Post Office',
'SG': 'Surgeon General',
'SSA': 'Social Security Act or Social Security Administration',
'TSA': 'Transportation Security Administration',
'TSC': 'Terrorist Screening Center',
'TSI': 'Transportation Safety Institute',
'USA': 'United States Army',
'USACE': 'U.S. Army Corps of Engineers',
'USAF': 'United States Air Force',
'USAFA': 'United States Air Force Academy',
'USMC': 'United States Marine Corp',
'USN': 'United States Navy',
'USPS': 'United States Postal Service',
'ACD': 'Advanced Counterfeit Deterrence',
'ACE': 'Automated Commercial Environment',
'ACES': 'Active Community Environments Initiative',
'AF': 'Administrative Function',
'AFDC': 'Aid to Families with Dependent Children',
'AHES': 'Average Hourly Earnings',
'AMW': 'Average Monthly Wage',
'ARS': 'Age, Race, Sex',
'BOD': 'Bid Opening Date',
'BRFSS': 'Behavioral Risk Factor Surveillance System',
'BRS': 'Biotechnology Regulatory Service',
'BY': 'Budget Year',
'CAPPS II': 'Computer Assisted Passenger Prescreening System',
'CARS': 'Car Allowance Rebate System',
'CB': 'Childrens Bureau',
'CBER': 'Center for Biologics Evaluation and Research',
'C/BR': 'Cost/Benefit Ratio, Cost/Burden Reduction',
'CD': 'Civil Defense',
'CPI': 'Consumer Price Index',
'DHRA': 'Defense Human Resources Activity',
'EDIE': 'Electronic Deposit Insurance Estimator',
'EEEL': 'Electronics and Electrical Engineering Laboratory',
'EERE': 'Energy Efficiency and Renewable Energy',
'FFY': 'Federal Fiscal Year',
'FINCEN': 'Financial Crimes Enforcement Network',
'FIPS': 'Federal Information Processing Standard',
'FISA': 'Federal Intelligence Surveillance Court',
'FMAP': 'Federal Medical Assistance Percentage',
'HIFCA': 'High Intensity Financial Crime Area',
'IFB or IFQ': 'Invitation for Bids, Invitation for Quote',
'MEPS': 'Medical Expenditure Panel Survey',
'MeSH': 'Medical Subject Headings',
'RFP or RFQ': 'Request for Proposal or Request for Quote',
'TRI': 'Toxics Release Inventory',
'AFK': 'Away From Keyboard',
'BBIAB': 'Be Back In A Bit',
'BBL': 'Be Back Later',
'BBS': 'Be Back Soon',
'BEG': 'Big Evil Grin',
'BRB': 'Be Right Back',
'BTW': 'By The Way',
'EG': 'Evil Grin',
'FISH': 'First In, Still Here',
'IDK': 'I Dont Know',
'IMO': 'In My Opinion',
'IRL': 'In Real Life',
'KISS': 'Keep It Simple, Stupid',
'LOL': 'Laughing Out Loud',
'NYOB': 'None of Your Business',
'OMG': 'Oh My God',
'PANS': 'Pretty Awesome New Stuff',
'PHAT': 'Pretty, Hot, And Tempting',
'POS': 'Parents Over Shoulder',
'TTYL': 'Talk To You Later',
}








print(reddit.user.me())

# Selecting the subreddit
subreddit = reddit.subreddit('politics')
tops = subreddit.top(limit=1)

# Browsing posts
for top_post in tops:
    title = top_post.title
    print("Title", title)
    comments = []

    # Browsing comments
    all_comments = top_post.comments.list()

    for comment in all_comments[:50]:
        comments.append(comment.body)
        # added this just for testing utf-8
        print (comment.body)
    pos_sent = []
    neg_sent = []
    comp_sent = []

    sid = SentimentIntensityAnalyzer()
    for comment in comments:
        score = sid.polarity_scores(comment)
        # print(comment, score['compound'])
        pos_sent.append(score['pos'])
        neg_sent.append(score['neg'])
        comp_sent.append(score['compound'])

    pos_sent = np.asarray(pos_sent)
    neg_sent = np.asarray(neg_sent)

    # Plotting
    plt.scatter(pos_sent, neg_sent, cmap='seismic', c=comp_sent)
    plt.show()

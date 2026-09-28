from pathlib import Path
import pandas as pd
import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

ROOT = Path(__file__).parent
SOURCE = ROOT / 'data' / 'raw' / 'bank' / 'bank-full.csv'
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)

df = pd.read_csv(SOURCE, sep=';')
df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 50, 65, np.inf], labels=['18-25', '26-35', '36-50', '51-65', '66+'])
df['subscribed'] = df['y']
df['campaign_contacts'] = df['campaign']
df.to_csv(OUT / 'campaign_customer_metrics.csv', index=False)

overall = df['subscribed'].eq('yes').mean() * 100
segment = df.groupby(['job', 'age_group'], observed=False).agg(contacts=('subscribed', 'size'), conversions=('subscribed', lambda s: (s == 'yes').sum())).reset_index()
segment['conversion_rate_pct'] = segment['conversions'] / segment['contacts'] * 100
segment = segment[segment['contacts'] >= 100].sort_values('conversion_rate_pct', ascending=False)
segment.to_csv(OUT / 'conversion_by_segment.csv', index=False)

contact = df.groupby('contact', dropna=False).agg(contacts=('subscribed', 'size'), conversions=('subscribed', lambda s: (s == 'yes').sum())).reset_index()
contact['conversion_rate_pct'] = contact['conversions'] / contact['contacts'] * 100
contact.to_csv(OUT / 'conversion_by_contact_method.csv', index=False)

campaign = df.groupby('campaign_contacts').agg(contacts=('subscribed', 'size'), conversions=('subscribed', lambda s: (s == 'yes').sum())).reset_index()
campaign['conversion_rate_pct'] = campaign['conversions'] / campaign['contacts'] * 100
campaign.to_csv(OUT / 'conversion_by_contact_count.csv', index=False)

print('CAMPAIGN CONTACTS:', len(df))
print('SUBSCRIPTIONS:', int((df['subscribed'] == 'yes').sum()))
print('OVERALL CONVERSION RATE (%):', round(overall, 2))
print('\nTOP CUSTOMER SEGMENTS - MINIMUM 100 CONTACTS')
print(segment.head(10).to_string(index=False))
print('\nCONVERSION BY CONTACT METHOD')
print(contact.to_string(index=False))

if plt is not None:
    top = segment.head(10).sort_values('conversion_rate_pct')
    top['segment'] = top['job'].astype(str) + ' / ' + top['age_group'].astype(str)
    top.plot.barh(x='segment', y='conversion_rate_pct', legend=False, title='Top Customer Segments by Conversion', figsize=(9, 5))
    plt.xlabel('Conversion rate (%)')
    plt.tight_layout()
    plt.savefig(OUT / 'conversion_by_segment.png', dpi=160)
    plt.close()

    campaign.head(15).plot(x='campaign_contacts', y='conversion_rate_pct', marker='o', legend=False, title='Conversion Rate by Number of Contacts', figsize=(8, 5))
    plt.xlabel('Number of campaign contacts')
    plt.ylabel('Conversion rate (%)')
    plt.tight_layout()
    plt.savefig(OUT / 'conversion_by_contact_count.png', dpi=160)
    plt.close()
else:
    print('\nCharts skipped: install dependencies from requirements.txt to generate PNG visualizations.')

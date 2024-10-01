import pandas as pd
import matplotlib.pyplot as plt

# Baca file CSV
df = pd.read_csv('backend_resp_time_v2.csv', delimiter='|')

# Mengambil 20 baris teratas berdasarkan kolom 'total_requests'
df = df.nlargest(20, 'total_requests')

# Pilih kolom untuk stacked columns (semua kolom kecuali 'backend_uri' dan 'total_requests')
columns_to_plot = df.columns[1:-1]

# Set backend_uri sebagai index
df.set_index('backend_uri', inplace=True)

# Hitung persentase dari setiap kolom (dari total_requests)
df_percent = df[columns_to_plot].div(df['total_requests'], axis=0) * 100

# Plot stacked bar chart dengan sumbu horizontal sebagai backend_uri dan sumbu vertikal sebagai persentase
df_percent.plot(kind='bar', stacked=True, figsize=(10, 7))

# Menambahkan label dan judul
plt.ylabel('Persentase Requests (%)')
plt.xlabel('Backend URI')
plt.title('Top 20 Total Request')
plt.legend(title='Rentang Waktu', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.savefig('top_20_total_requests.pdf', format='pdf')
# Tampilkan diagram
plt.show()

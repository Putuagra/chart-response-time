import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

csv_file = 'output.csv'
df = pd.read_csv(csv_file, delimiter='|')

def generateResponseTime(the_data, typeUri):
    # Define response time intervals (bins) for categorizing the response times
    bins = [2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, np.inf]  # np.inf for values greater than 10 seconds
    labels = ['2s-3s', '3s-4s', '4s-5s', '5s-6s', '6s-7s', '7s-8s', '8s-9s', '9s-10s', '>10s']

    if typeUri == 'backend':
        # Create a new column for binned response times
        the_data['response_time_interval'] = pd.cut(the_data['backend_exec_time'], bins=bins, labels=labels, right=False)
        grouped = the_data.groupby(['backend_uri', 'response_time_interval']).size().unstack(fill_value=0)
        grouped['total_requests'] = grouped[['2s-3s', '3s-4s', '4s-5s', '5s-6s', '6s-7s', '7s-8s', '8s-9s', '9s-10s', '>10s']].sum(axis=1)
        grouped = grouped.reset_index()
        df_sorted = grouped.sort_values(by='total_requests', ascending=False)
        # df_sorted.to_csv('backend_resp_time.csv', sep='|')
        # print(df_sorted)
        return df_sorted
    elif typeUri == 'surrounding':
        # Create a new column for binned response times
        the_data['response_time_interval'] = pd.cut(the_data['surr_exec_time'], bins=bins, labels=labels, right=False)
        grouped = the_data.groupby(['surr_uri', 'response_time_interval']).size().unstack(fill_value=0)
        grouped['total_requests'] = grouped[['2s-3s', '3s-4s', '4s-5s', '5s-6s', '6s-7s', '7s-8s', '8s-9s', '9s-10s', '>10s']].sum(axis=1)
        grouped = grouped.reset_index()
        df_sorted = grouped.sort_values(by='total_requests', ascending=False)
        # df_sorted.to_csv('backend_resp_time.csv', sep='|')
        # print(df_sorted)
        return df_sorted
    
def generateChart(df,typeUri,pdfName):
    df = df.nlargest(20, 'total_requests')

    # Pilih kolom untuk stacked columns (semua kolom kecuali '*_uri' dan 'total_requests')
    columns_to_plot = df.columns[1:-1]

    # Set type_uri sebagai index
    if typeUri == 'Backend':
        df.set_index('backend_uri', inplace=True)
    elif typeUri == 'Surrounding':
        df.set_index('surr_uri', inplace=True)

    # Hitung persentase dari setiap kolom (dari total_requests)
    df_percent = df[columns_to_plot].div(df['total_requests'], axis=0) * 100

    # Plot stacked bar chart dengan sumbu horizontal sebagai type_uri dan sumbu vertikal sebagai persentase
    df_percent.plot(kind='bar', stacked=True, figsize=(10, 7))

    # Menambahkan label dan judul
    plt.ylabel('Persentase Requests (%)')
    plt.xlabel(f'{typeUri} URI')
    plt.title(f'Top 20 Total Request {typeUri}')
    plt.legend(title='Rentang Waktu', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.savefig(pdfName, format='pdf')
    # Tampilkan diagram
    # plt.show()
    
if __name__ == "__main__":
    print("Running.....")
    df_backend = generateResponseTime(df, "backend")
    df_surr = generateResponseTime(df, "surrounding")
    # print(df_backend)
    generateChart(df_backend,'Backend','top_20_total_requests_backend.pdf')
    generateChart(df_surr,'Surrounding','top_20_total_requests_surrounding.pdf')
    # print(df_surr)
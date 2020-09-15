import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
# import streamlit.components.v1 as components



connection = mysql.connector.connect(host='localhost',
                            database='belajar',
                            user='root',
                            password='')
cursor = connection.cursor()

def add_data(NPP,Date,Nama_pegawai,Jenis_Kelamin,Status_Relasi,Status,Status_Sehat_Update,Indikasi,Tindakan_Penanganan,Lokasi_Penanganan,Tanggal_Akhir,Unit_Kerja,Keterangan,Status_Akhir):
    if Status=="PDP":
        PDP="1"
        ODP="0"
        Sehat="0"
    elif Status=="ODP":
        PDP="0"
        ODP="1"
        Sehat="0"
    elif Status=="Sehat":
        PDP="0"
        ODP="0"
        Sehat="1"
    try:
            cursor.execute("INSERT INTO tbl_covid (NPP,Date, Nama, Jenis_Kelamin,Status_Relasi,Status,Status_Sehat_Update,Indikasi,Tindakan_Penanganan,Lokasi_Penanganan,Date_Akhir,Unit_Kerja,Keterangan,Status_Akhir) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (NPP,Date,Nama_pegawai,Jenis_Kelamin,Status_Relasi,Status,Status_Sehat_Update,Indikasi,Tindakan_Penanganan,Lokasi_Penanganan,Tanggal_Akhir,Unit_Kerja,Keterangan,Status_Akhir))
            # cursor.execute("INSERT INTO tbl_lineplot (Date, PDP,ODP,Sehat) VALUES (%s,%s,%s,%s)", (Date, PDP, ODP, Sehat))
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into Laptop table")
            cursor.close()

    except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))

    finally:
            if (connection.is_connected()):
                connection.close()
                print("MySQL connection is closed")



# Layout Template
html_temp = """
<div style="background-color:{};padding:10px;border-radius:10px">
<h3 style="color:{};text-align:center;">Input kasus terbaru covid </h3>
</div>
"""
covid_temp = """
<div style="background-color:{};padding:10px;border-radius:10px">
<h3 style="color:{};text-align:center;">Dashboard Satgas Covid JM</h3>
</div>
<br>
"""
def hitung_PDP():
    sql_select_query = """SELECT count(status) FROM `tbl_covid` where status='PDP'  """
    cursor.execute(sql_select_query)
    record_PDP = cursor.fetchone()
    return int(record_PDP[0])

# def jumlah_anak_PDP():
#     sql_select_query = """SELECT sum(Jumlah_Anak) FROM `tbl_covid` where Status_Anak='PDP'  """
#     cursor.execute(sql_select_query)
#     record_jumlah_anak_PDP = cursor.fetchone()
#     return int(record_jumlah_anak_PDP[0])

# def jumlah_istri_PDP():
#     sql_select_query = """select count(Status_Istri) from tbl_covid where Status_Istri='PDP' """
#     cursor.execute(sql_select_query)
#     record_istri_PDP = cursor.fetchone()
#     return int(record_istri_PDP[0])

def hitung_ODP():
    sql_select_query = """SELECT count(status) FROM `tbl_covid` where status='ODP'  """
    cursor.execute(sql_select_query)
    record_ODP = cursor.fetchone()
    return int(record_ODP[0])

# def jumlah_anak_ODP():
#     sql_select_query = """SELECT sum(Jumlah_Anak) FROM `tbl_covid` where Status_Anak='ODP'  """
#     cursor.execute(sql_select_query)
#     record_jumlah_anak_ODP = cursor.fetchone()
#     return int(record_jumlah_anak_ODP[0])

# def jumlah_istri_ODP():
#     sql_select_query = """select count(Status_Istri) from tbl_covid where Status_Istri='ODP' """
#     cursor.execute(sql_select_query)
#     record_istri_ODP = cursor.fetchone()
#     return int(record_istri_ODP[0])

def hitung_Sehat():
    sql_select_query = """SELECT count(status) FROM `tbl_covid` where status='Sehat'  """
    cursor.execute(sql_select_query)
    record_Sehat = cursor.fetchone()
    return int(record_Sehat[0])

# def jumlah_anak_Sehat():
#     sql_select_query = """SELECT sum(Jumlah_Anak) FROM `tbl_covid` where Status_Anak='Sehat'  """
#     cursor.execute(sql_select_query)
#     record_jumlah_anak_Sehat = cursor.fetchone()
#     return int(record_jumlah_anak_Sehat[0])

# def jumlah_istri_Sehat():
#     sql_select_query = """select count(Status_Istri) from tbl_covid where Status_Istri='Sehat' """
#     cursor.execute(sql_select_query)
#     record_istri_Sehat = cursor.fetchone()
#     return int(record_istri_Sehat[0])

def Query_Barchart():
    df_barchart = pd.read_sql('select Unit_Kerja, count(Unit_Kerja) as jumlah_kasus from tbl_covid GROUP BY Unit_Kerja', con=connection)
    sumbu_x=df_barchart["Unit_Kerja"].values.tolist()
    sumbu_y=df_barchart["jumlah_kasus"].values.tolist()
    return sumbu_x,sumbu_y

# def Query_Barchart():
#     df_barchart = pd.read_sql('select Unit_Kerja, count(Unit_Kerja) as jumlah_kasus from tbl_covid GROUP BY Unit_Kerja', con=connection)
#     sumbu_x=df_barchart["Unit_Kerja"].values.tolist()
#     sumbu_y=df_barchart["jumlah_kasus"].values.tolist()
#     return sumbu_x,sumbu_y

def main():
	st.sidebar.title("Dashboard Statistics")
	st.sidebar.write("JasaMarga Fight Covid")
	st.sidebar.error("Karyawan PDP : " +"   "+ str(hitung_PDP())+"  Orang")
	st.sidebar.warning("Karyawan ODP : " +"   "+ str(hitung_ODP())+"  Orang")
	st.sidebar.info("Karyawan Sembuh : " +"   "+ str(hitung_Sehat())+"  Orang")

	option=st.sidebar.selectbox('Pilih Menu',('Input Kasus','Daftar Kasus','Update Kasus'))

	if option=='Input Kasus':
			st.title("Input Kasus Terbaru")
			st.write("""Input kasus ini berguna untuk mengetahui tingkat penyebaran covid 19 lingkungan PT Jasa Marga (Persero) Tbk""")
			Date = st.date_input("Tanggal Laporan")
			Nama_pegawai = st.text_input("Nama Pegawai")
			NPP = st.text_input("NPP Pegawai")
			Jenis_Kelamin = st.radio("Jenis Kelamin",("Laki-Laki","Perempuan"))
			Status = st.selectbox("Status Kesehatan Pegawai",("PDP","ODP","Sehat"))
			Status_Relasi= st.radio("Status Karyawan",("Operasional","Non Operasional","Magang"))
			Unit_Kerja=st.selectbox("Unit Kerja",("Kantor Pusat","JMTO","JMTM","JMRB",
					"JBT","JSB","JSM","MSJ","JCC","MLJ","JKC","JMKT","TMJ",
					"JMB","JSN","JPM","JGP","JPB","JTT","Regional"))
			Indikasi = st.text_area("Jelaskan Keluhan dan Indikasi yang dirasakan","""
			
			
			""")
			Tindakan_Penanganan= st.radio("Tindakan Penanganan",("Isolasi Mandiri","Karantina"))
			Lokasi_Penanganan = st.text_input("Lokasi Penanganan")
			Tanggal_Akhir = st.date_input("Masukan Tanggal Akhir Penanganan")
			Keterangan = st.text_input("Keterangan")
			Status_Akhir = st.selectbox("Status Akhir",("Sehat","Lanjut Isolasi Mandiri","Menunggu Swab","Menunggu Rapid"))
			st.text("Wajib verifikasi dibawah ini")
			Status_Sehat_Update="0"
			Verifikasi = st.checkbox('Data yang sudah saya masukan adalah benar')
			if st.button("Tambah"):
				if Verifikasi == True: 
					add_data(NPP,Date,Nama_pegawai,Jenis_Kelamin,Status_Relasi,Status,Status_Sehat_Update,Indikasi,Tindakan_Penanganan,Lokasi_Penanganan,Tanggal_Akhir,Unit_Kerja,Keterangan,Status_Akhir)
					st.success("Berhasil Disimpan")
                    
	elif option=='Daftar Kasus':
            st.markdown(covid_temp.format('royalblue','white'),unsafe_allow_html=True)

            st.subheader("Daftar Kasus")
            df = pd.read_sql('SELECT * FROM tbl_covid', con=connection)
            df_lineplot = pd.read_sql('SELECT Date,count(PDP) as PDP, count(ODP) as ODP, count(Sehat) as Sehat  FROM `tbl_lineplot` GROUP BY Date', con=connection)
            st.dataframe(df)

            st.subheader("Total Kasus Harian")
            st.table(df_lineplot)


            df_lineplot['Date']=pd.to_datetime(df_lineplot['Date'])
            
            st.subheader("Jumlah kasus Covid di Jasa Marga")
            sumbu_x,sumbu_y=Query_Barchart()
            fig1 = go.Figure(data=[go.Bar(
                        x=sumbu_x, y=sumbu_y,
                        textposition='auto',
                    )])
            st.plotly_chart(fig1)

            fig = px.line(df_lineplot, x='Date', y=df_lineplot.columns,
              title='Perbandingan Kasus covid 19')
            fig.update_xaxes(
                dtick="M1",
                tickformat="%b %Y")

            st.plotly_chart(fig)

            df =pd.read_excel("C:/Users/Ganteng/Music/supervised_learning-master/Medina/datacovid.xls",parse_dates=True, squeeze=True)
            df1 =pd.read_excel("C:/Users/Ganteng/Music/supervised_learning-master/Medina/datacovidkantor.xls")
        
            y_pdp=df1["PDP"].values.tolist()
            y_odp=df1["ODP"].values.tolist()
            y_total=df1["Total"].values.tolist()
            x=['Kantor Pusat','JMTO','JMTM','JMRB','JBT','JSB','JSM',
            'MSJ','JJC','MLJ','JKC','JMKT','TMJ','JMB','JSN',
            'JPM','JGP','JPB','JTT','Regional']

            df['Date']=pd.to_datetime(df['Date'])

            options = st.multiselect(
            'What are your favorite colors',
            ['Green', 'Yellow', 'Red', 'Blue'],
            ['Yellow', 'Red'])
            st.write('You selected:', options)
            st.text(options)

            agree = st.checkbox('I agree')
            st.text(agree)

            option = st.selectbox(
            'How would you like to be contacted?',
            ('Email', 'Home phone', 'Mobile phone'))
            st.write('You selected:', option)
            st.text(option)

	elif option=='Update Kasus':
		st.title("Update Kasus Terbaru")
		st.write("""Update kasus ini berguna untuk mengetahui tingkat kesembuhan Covid 19 pegawai PT Jasa Marga(Persero) Tbk""")
		Nama_pegawai = st.text_input("Nama Pegawai")
		NPP = st.text_input("NPP Pegawai")
		Berubah_Sehat = st.checkbox('Status Berubah Menjadi Sehat')
		Verifikasi_Sehat = st.checkbox('Data yang Saya Inputkan Benar')
		if (st.button("Update Data")):
			if (Verifikasi == True):
				# update_data(Tanggal_kasus,Nama_pegawai,Status_Kesehatan,NPP,Jenis_Kelamin,Status_Relasi
				# ,Unit_kerja,)
				st.success("Berhasil Disimpan")
if __name__ == '__main__':
	    main()
 

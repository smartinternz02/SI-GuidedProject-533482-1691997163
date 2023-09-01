


    
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wbj37866;PWD=1RztLEHwRBEgrMb1",'','')
print(conn)
print("connection successful...")

sql="select * from assignment"
stmt=ibm_db.exec_immediate(conn, sql)
row = ibm_db.fetch_tuple(stmt)        
print(row)

while row != False:
    print(row[0]," ",row[1]," ",row[2],"\n")
    row = ibm_db.fetch_both(stmt)



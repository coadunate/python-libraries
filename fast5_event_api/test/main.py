import h5py

fh = h5py.File("SKSASKA671342P_20170221_FNFAF11800_MN20421_mux_scan_Lambda_1_51925_ch467_read53_strand.fast5",'r')

data = fh['Raw/Reads/Read_53/Signal'][13]

print(data)

#for i in data:
#    print(i)



library(ncdf4)


for(scen in c("low","high")){

nc= nc_open(paste0("ENS_knmi_NORTHSEA_slscen_",scen,".nc"))

dat= list()
for(vname in names(nc$var)){
	dat[[vname]] = ncvar_get(nc,vname)
}
nvar=length(names(dat))
nc_close(nc)

pdf(paste0("testplot_",scen,".pdf"),width=10,height=8)
par(mfrow=c(3,nvar/3))
for(vname in names(dat)){
	plot(dat[[vname]][1,],main=vname,type="l")
	for(jline in 1:7){
		lines(dat[[vname]][jline,],col=jline)
	}
	legend("topleft",paste(1:7),col=1:7,lty=1,cex=0.5)
}
dev.off()
}


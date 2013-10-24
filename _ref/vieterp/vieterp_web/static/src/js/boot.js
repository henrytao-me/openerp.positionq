/*---------------------------------------------------------
 * VietERP Web web module split
 *---------------------------------------------------------*/
openerp.vieterp_web = function(session) {
    for(var key in openerp.vieterp_web) {
        if(openerp.vieterp_web[key]) {
            openerp.vieterp_web[key](session);
        }
    }
};

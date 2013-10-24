openerp.vieterp_web_graph = function (instance) {



var _t = instance.web._t;
var _lt = instance.web._lt;
var QWeb = instance.web.qweb;



instance.web_graph.GraphView.include({
	init: function(){
		var self = this;
		this._super.apply(this, arguments);
	},
	view_loading: function(){
		var self = this;
		//add container
		this.$el.wrap($('<div class="oe_form_sheetbg"><div class="oe_form_sheet oe_form_sheet_width"></div></div>'));		
		//
		this._super.apply(this, arguments);	
	}
});



};

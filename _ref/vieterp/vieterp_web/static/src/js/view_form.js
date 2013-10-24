/* Vieter View Form
 * 1. Filter on many2many, many2one field: <field name="users" domain="[('is_public', '=', True)]" filter="[('is_public', '=', True)]" />
 */

openerp.vieterp_web.view_form = function (instance) {



var _t = instance.web._t;
var _lt = instance.web._lt;
var QWeb = instance.web.qweb;


instance.web.form.FieldStatus.include({
	on_click_stage: function(ev){
		var self = this;
        var $li = $(ev.currentTarget);        
        var val = parseInt($li.data("id"));        
        val = $li.data('id');        
        if (val != self.get('value')) {
            this.view.recursive_save().done(function() {
                var change = {};
                change[self.name] = val;
                self.view.dataset.write(self.view.datarecord.id, change).done(function() {
                    self.view.reload();
                });
            });
        }
	}
});



instance.web.FormView.include({
	init_pager: function(){
		try{
			//this.options.$pager.empty();
			this.options.$pager.find('.oe_list_pager').hide();	
		}catch(ex){};
		this._super.apply(this, arguments);
		// this.view_form.on("form_view_loaded", self, function() {
		
	},
	load_form: function(data){
		var self = this;
		this._super.apply(this, arguments);
		//check header
		this.$el.find('header').append('<div class="clearfloat" style="height:0px;">');
	}
});



instance.web.form.FieldMany2Many.include({
	initialize_content: function() {
        var self = this;

        this.$el.addClass('oe_form_field oe_form_field_many2many');
        
        var filter = self.node.attrs.filter;
	
        this.list_view = new instance.web.form.Many2ManyListView(this, this.dataset, false, {
                    'addable': this.get("effective_readonly") ? null : _t("Add"),
                    'deletable': this.get("effective_readonly") ? false : true,
                    'selectable': this.multi_selection,
                    'sortable': false,
                    'reorderable': false,
                    'import_enabled': false,
                    'filter': filter
            });
        var embedded = (this.field.views || {}).tree;
        if (embedded) {
            this.list_view.set_embedded_view(embedded);
        }
        this.list_view.m2m_field = this;
        var loaded = $.Deferred();
        this.list_view.on("list_view_loaded", this, function() {
            loaded.resolve();
        });
        this.list_view.appendTo(this.$el);

        var old_def = self.is_loaded;
        self.is_loaded = $.Deferred().done(function() {
            old_def.resolve();
        });
        this.list_dm.add(loaded).then(function() {
            self.is_loaded.resolve();
        });
    },
});


};

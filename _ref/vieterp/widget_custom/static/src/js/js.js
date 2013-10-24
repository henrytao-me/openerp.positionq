/*---------------------------------------------------------
 * VietERP widget_custom
 * Usage:
 * 1. trigger: widget_custom.reloaded
 *---------------------------------------------------------*/

openerp.widget_custom = function(instance){

var QWeb = instance.web.qweb;

instance.web.form.widgets.add('widget_custom', 'instance.web.form.widget_custom');
instance.web.form.widget_custom = instance.web.form.AbstractField.extend(instance.web.form.ReinitializeFieldMixin, {
    template: 'form_widget_custom',
    _model: null,
	_context: null,
	_id: 0,
	_template_name: 'form_widget_custom.template_name',
	_template_data: null,
	
    init: function (field_manager, node) {
    	var self = this;
        this._super(field_manager, node);
    },
    
    initialize_content: function() {
    	
    },
    
    getEx: function(key){
    	var res = null;
    	switch(key){
    	case 'model':
    		res = this._model;
    		break;
    	case 'id':
    		res = this._id;
    		break;
    	case 'template_name':
    		res = this._template_name;
    		break;
    	case 'template_data':
    		res = this._template_data;
    		break;
    	};
    	return res
    },
    
    render_value: function(){
    	var self = this;
    	
    	self._model = new instance.web.Model(self.view.dataset.model);
    	var context = this.build_context().__eval_context.__contexts[1];
    	self._id = context.id;
    	self._template_name = self.node.attrs.template_name || '';
    	self._template_data = self.node.attrs.template_data || '';
    	
    	self.reload_custom(); 
    },
    
    reload_custom: function(callback){
    	var self = this;
    	try{
    		callback = callback || function(){};
    		if(self._template_data){
	    		self._model.call(self._template_data, [self._id]).then(function(data, status){
	    			self.render_custom(data);
	    			callback();
	    		});	
    		}else{
    			self.render_custom({'data': []});
    			callback();
    		};
    	}catch(ex){}
    },
    
    render_custom: function(data){
    	var self = this;    	
    	var $data = $(QWeb.render(self._template_name, {
			template_data: data
		}));
    	self.$('.form_widget_custom_container').empty().append($data);    			
		$(window).trigger('widget_custom.reloaded', [{view: self, data: data, $this: $data}]);
    },
    
    init_event: function(){
    	
    },
    
    on_editing: function(){
    	
    },
    
});

}

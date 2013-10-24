openerp.widget_poll = function(instance){
	var QWeb = instance.web.qweb;
	
	instance.web.form.widgets.add('widget_poll', 'instance.web.form.widget_poll');
	instance.web.form.widget_poll = instance.web.form.AbstractField.extend(instance.web.form.ReinitializeFieldMixin, {
	    template: 'widget_poll',	    
	    _model: '', 	    
		
		_func_read: "poll_read",
		_func_add: "poll_add",
		_func_save: "poll_save",
		
		_id: 0,
		
		_context: null,
		
		_new_data: {},
		
		_t_edit: 'Editing',
		_t_save: 'Saved',
		_t_add: 'Add',
		_t_refresh: 'Refresh',
		$button: {},
		
	    init: function (field_manager, node) {
	    	var self = this;
	        this._super(field_manager, node);
	    },
	    
	    initialize_content: function() {
	    	
	    },
	    
	    render_value: function(){
	    	var self = this
	    	//init attrs	        
	        self._model = new instance.web.Model(self.view.dataset.model);
	        self._func_read = self.node.attrs.func_read;
	        self._func_add = self.node.attrs.func_add;
	        self._func_save = self.node.attrs.func_save;
	        self._t_edit = self.node.attrs.t_edit || self._t_edit;
	        self._t_save = self.node.attrs.t_save || self._t_save;
	        self._t_add = self.node.attrs.t_add || self._t_add;
	        self._t_refresh = self.node.attrs.t_refresh || self._t_refresh; 
	        //get context	        
	        // instance.web.pyeval.eval_domains_and_contexts({		            
	            // contexts: this.build_context() || [],		            
	        // }).done(function (results) {
	        	// self._context = results.context;		        	
	        // });
	        //get active id	        
	        context = this.build_context().__eval_context.__contexts[1];
    		self._id = context.id;
    		
	    	//init button
	    	self.$button = {
	    		add: self.$('.poll_button_add'),
	    		save: self.$('.poll_button_save'),
	    		refresh: self.$('.poll_button_refresh')
	    	};
	    	self.init_event();
	    	//reload poll
	    	self.reload_poll();
	    },
	    
	    init_event: function(){
	    	var self = this;
	    	self.$button['add'].click(function(){
	    		try{
		    		self._model.call(self._func_add, [self._id]).then(function(data, status){
		    			self.reload_poll();
		    		});
		    	}catch(ex){}
	    	});
	    	self.$button['save'].click(function(){
	    		try{
		    		self._model.call(self._func_save, [self._id, self.get_new_data()]).then(function(data, status){
		    			self.reset_new_data();
		    			self.reload_poll();
		    		});
		    	}catch(ex){}
	    	});
	    	self.$button['refresh'].click(function(){
	    		self.reload_poll();
	    	});
	    },
	    
	    get_new_data: function(){
	    	var self = this;
	    	var res = []
			for(var ver_id in self._new_data){
				var tmp = self._new_data[ver_id];
				tmp['ver_id'] = ver_id;
				res.push(tmp);
			}
			return res;
	    },
	    
	    reset_new_data: function(){
	    	var self = this;
	    	self._new_data = {};
	    },
	    
	    reload_poll: function(callback){
	    	var self = this;
	    	try{
	    		callback = callback || function(){};
	    		self._model.call(self._func_read, [self._id]).then(function(data, status){
	    			self.render_poll(data);
	    			//
	    			self.reload_poll_complete();  
	    			//caclback
	    			callback();
	    		});
	    	}catch(ex){}
	    },
	    
	    reload_poll_complete: function(){
	    	var self = this;
	    	self.$button['save'].html(self._t_save);
	    },
	    
	    on_editing: function(){
	    	var self = this;
	    	self.$button['save'].html(self._t_edit);
	    },
	    
	    render_poll: function(data){
	    	var self = this;
	    	data = $.ekit.initData(data, {
	    		hoz_cols: [],
	    		ver_cols: [],
	    		data: []
	    	})
	    	var $table = $(instance.web.qweb.render('widget_poll.table', data));
	    	self.$('.container').empty().append($table);
	    	//init readonly and checked
	    	for(row in data.data){
	    		for(col in data.data[row]){
	    			ver_id = data.data[row][col].ver_id;
	    			hoz_id = data.data[row][col].hoz_id;
	    			readonly = data.data[row][col].readonly || false;
	    			value = data.data[row][col].value;
	    			type = data.data[row][col].type;
	    			//readonly
	    			if(readonly === true){
	    				self.$('.poll_input[data-ver-id="'+ver_id+'"][data-hoz-id="'+hoz_id+'"]').attr('readonly', 'readonly').attr('disabled', 'disabled');
	    			}
	    			//checked
	    			if(type === 'radio' && value === true){
	    				self.$('.poll_input[data-ver-id="'+ver_id+'"][data-hoz-id="'+hoz_id+'"]').attr('checked', 'checked');
	    			}
	    		}
	    	};
	    	//init event
	    	var $radio_parent = self.$('.container .poll_content .poll_row .poll_cell input[type="radio"]').parent();
	    	if($radio_parent.is('.poll_cell')){
	    		$radio_parent.click(function(e){
	    			if($(this).children('input[type="radio"]').is(':checked') || $(this).attr('data-type') != 'radio' || $(this).children('input[type="radio"]').is(':disabled')){
	    				return;	
	    			};
	    			$(this).children('input[type="radio"]').attr('checked', 'checked');
	    			$(this).children('input[type="radio"]').trigger('change');
	    			e.stopPropagation();
	    		});
	    	};
	    	self.$('.container .poll_content .poll_row .poll_cell input[type="radio"]').change(function(){
	    		ver_id = $(this).attr('data-ver-id');
	    		hoz_id = $(this).attr('data-hoz-id');
	    		type = $(this).attr('data-type');
	    		
	    		self._new_data[ver_id] = {
	    			hoz_id: hoz_id,
	    			type: type
	    		};
	    		//remove all textbox value
	    		self.$('.container .poll_content .poll_row .poll_cell input[type="textbox"][data-ver-id="'+ver_id+'"]').val('');
	    		self.on_editing();
	    	});
	    	self.$('.container .poll_content .poll_row .poll_cell input[type="textbox"]').click(function(){
	    		ver_id = $(this).attr('data-ver-id');
	    		hoz_id = $(this).attr('data-hoz-id');
	    		type = $(this).attr('data-type');
	    		
	    		// $(this).parent().children('input[type="radio"]').attr('checked', 'checked');
	    	});
	    	self.$('.container .poll_content .poll_row .poll_cell input[type="textbox"]').change(function(){
	    		$(this).parent().children('input[type="radio"]').attr('checked', 'checked');
	    		
	    		ver_id = $(this).attr('data-ver-id');
	    		hoz_id = $(this).attr('data-hoz-id');
	    		type = $(this).attr('data-type');
	    		value = $(this).val();
	    		
	    		self._new_data[ver_id] = {
	    			hoz_id: hoz_id,
	    			type: type,
	    			value: value	    			
	    		};
	    		self.on_editing();
	    	});
	    }
	});
}

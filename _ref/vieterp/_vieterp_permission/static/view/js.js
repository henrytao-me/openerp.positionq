openerp.vieterp_permission = function (instance) {

var _t = instance.web._t;
var _lt = instance.web._lt;
var QWeb = instance.web.qweb;

$(window).bind('list.custom.load_list', function(e, trigger){
	try{
		var view = trigger.view;
		var model = view.model;
		if(model == 'v.access'){
			var $buttons = view.options.$buttons;
			//process
			if(!$buttons.find('.btn_access_process').isExist()){
				var model = new instance.web.Model('v.access');
				model.call('get_status', []).then(function(data, status){
					status = data;
					var state = {
						0: 'Chờ cập nhật',
						1: 'Đang cập nhật...',
						2: 'Sẵn sàng'
					};
					var $process = $('<button type="button"></button>')
						.addClass('btn_access_process oe_button')
						.html(state[status]);
					$process.v_change_status = function(status){
						if(status == 2){
							$process.attr("disabled", "disabled")
							 		.removeClass('oe_highlight')
							 		.html(state[status]);
						}else{
							$process.removeAttr("disabled")
							 		.addClass('oe_highlight')
							 		.html(state[status]);
						};
					};
					$process.v_change_status(status);
					//
					$process.click(function(){
						if(status == 2){
							return;
						}else if(status == 0){
							$process.v_change_status(1);
						};
						model.call('process_access', []).then(function(data, status){
							$process.v_change_status(data);
						});
					});
					$buttons.append($process);				
				});
			}			
		};	
	}catch(ex){};
});

$(window).bind('list.custom.body.init', function(e, trigger){
	try{
		var $el = trigger.$el;
		var $body = trigger.$body;
		var view = trigger.view;
		//check vieterp_permission
		if(!$el.find('table.vieterp_permission').isExist()){
			return;
		}
		$body.delegate('.btn_perm', 'click', function(e){
			//check click prev
			var clicking = $el.data('click') || false;
			if(clicking == true){
				return;
			}
			clicking = true;
			$el.data('click', clicking);			
			//get info
			var $parent = $(this).parent();
			var data_value = parseInt($parent.attr('data-value')) + 1;
			var data_id = $parent.attr('data-id');
			var data_field = $parent.attr('data-field');
			//add class
			$parent.addClass('perm_container');
			//change permission in ui
			if(data_value > 2){
				data_value = 0;
			};
			$parent.attr('data-value', data_value);			
			//call on server
			var model = new instance.web.Model('v.access');
			model.call('change_permission', [data_id, data_field, data_value, data_id, view.dataset.context]).then(function(data, status){
				$el.data('click', false);
				for(var id in data){
					$el.find('.perm_container[data-field="'+data_field+'"][data-id="'+id+'"]')
						.attr('data-real-value', data[id]['real_'+data_field]);
				};				
			});
		});
	}catch(ex){}
});


$(window).bind('list.custom.group_header.add', function(e, trigger){
	try{
		var $row = trigger.$row;
		var $el = trigger.$el;
		var view = trigger.view;
		var group = trigger.group;
		var domain = group.domain;
		//check vieterp_permission
		if(!$el.find('table.vieterp_permission').isExist()){
			return;
		};
		//init domain
		var bak = [];
		for(var i in domain){
			if(domain[i][0] != 'level'){
				bak.push(domain[i]);
			};
		};
		domain = bak;
		//call on server
		var model = new instance.web.Model('v.access');
		model.call('get_group_permission', [domain, {}]).then(function(data, status){
			//add element
			var ls = ['perm_read', 'perm_write', 'perm_create', 'perm_unlink', 'perm_manage'];
			$row.attr('data-id', data['id'] || '0');
			for(var i in ls){
				$row.find('td[data-field="'+ls[i]+'"]')
					.empty()
					.attr('data-id', data['id'] || '0')
					.attr('data-value', data[ls[i]] || '0')
					.attr('data-real-value', data['real_'+ls[i]] || 'false')				
					.append($('<input type="button" class="btn_perm"></input>'));	
			};			
			//add class perm_container
			$row.find('.btn_perm').parent().addClass('perm_container');
			//init event
			$row.find('.btn_perm').bind('click', function(e){
				e.stopPropagation();
				//check click prev
				var clicking = $el.data('click') || false;
				if(clicking == true){
					return;
				}
				clicking = true;
				$el.data('click', clicking);
				//get info
				var $parent = $(this).parent();
				var data_value = parseInt($parent.attr('data-value')) + 1;
				var data_id = $parent.attr('data-id');
				var data_field = $parent.attr('data-field');				
				//change permission in ui
				if(data_value > 2){
					data_value = 0;
				};
				$parent.attr('data-value', data_value);
				//get return_ids
				return_ids = [];
				$el.find('tbody > tr').each(function(){
					return_ids.push($(this).attr('data-id'));
				});				
				//call on server
				var model = new instance.web.Model('v.access');
				model.call('change_permission', [data_id, data_field, data_value, return_ids, view.dataset.context]).then(function(data, status){
					$el.data('click', false);
					for(var id in data){
						$el.find('.perm_container[data-field="'+data_field+'"][data-id="'+id+'"]')
							.attr('data-real-value', data[id]['real_'+data_field]);
					};				
				});				
			});
		});
	}catch(ex){}
});

};

// JavaScript Document http://www.w3schools.com/js/tryit.asp?filename=tryjs_variables
// ekit ui - easy toolkit ui framework
// compatible with jquery 1.7.2
/**
 * ReplaceAll by Fagner Brack (MIT Licensed)
 * Replaces all occurrences of a substring in a string
 */
String.prototype.replaceAll = function( token, newToken, ignoreCase ) {
    var _token;
    var str = this + "";
    var i = -1;

    if ( typeof token === "string" ) {

        if ( ignoreCase ) {

            _token = token.toLowerCase();

            while( (
                i = str.toLowerCase().indexOf(
                    token, i >= 0 ? i + newToken.length : 0
                ) ) !== -1
            ) {
                str = str.substring( 0, i ) +
                    newToken +
                    str.substring( i + token.length );
            }

        } else {
            return this.split( token ).join( newToken );
        }

    }
return str;
};

$(function(){	
	///////////////////////////////////////
	//$$ - support array selector
	var $$ = function(selector){
		if($.isArray(selector)){
			var tmp = "";
			for(var i in selector){
				tmp += selector[i] + ' ';
			};
			selector = tmp;
		};
		return $(selector);
	};
	window.$$ = $$;
	///////////////////////////////////////
	//isExist
	$.fn.isExist = function(){
		var length = $(this).length;
		if(length == 0){
			return false;
		};
		return true;	
	};
	///////////////////////////////////////
	//isHide
	$.fn.isHide = function(){
		if($(this).css('display') == 'none'){
			return true;
		};
		return false;	
	};
	///////////////////////////////////////
	//isShow
	$.fn.isShow = function(){
		return !$(this).isHide();	
	};
	///////////////////////////////////////
	//message
	$.fn.message = function(opt){
		opt = $.ekit.initData(opt, {
			modal: true,
			resizable: false,
			show: {
				effect: 'drop',
				direction: 'up',
				duration: 400
			},
			hide: {
				effect: 'drop',
				direction: 'up',
				duration: 200
			},
			draggable: false,
			closeOnEscape: true,
			minWidth: '300px',
			buttons: {
				'OK': function(){
					$(this).dialog('close');	
				}
			}
		});
		$(this).dialog(opt);
	};
	///////////////////////////////////////
	//outerHtml
	$.fn.outerHtml = function(){
		return $('<div>').append($(this).clone()).html();
	};
	///////////////////////////////////////
	//reloadHtmlObj
	$.fn.reloadHtmlObj = function(){
		if(!$.ekit.isset(this.me)){
			return this;
		}
		var tmp = $(this.me);
		tmp.me = this.me;
		tmp.$ = this.$;
		for(var i in tmp.$){
			tmp['$'+i] = tmp.$[i];
		}
		return tmp;
	}
	///////////////////////////////////////
	//upgrade bind
	$.fn.__bind = function(types, fn, option){
		var func = function(e, trigger){
			e.trigger = trigger;
			fn.call(this, e, option);
		};
		return this.bind(types, func);
	};
	///////////////////////////////////////
	//upgrade each
	$.fn.__each = function(func, option){
		func = func || function(){};
		option = option || {};
		var maxIndex = $(this).length - 1;		
		return $(this).each(function(e){
			func.call(this, {
				index: e,
				length: maxIndex + 1,
				isEnd: (e==maxIndex?true:false)	
			}, option);
		});
	};
	///////////////////////////////////////
	//setID
	$.fn.setID = function(id, force){
		if(!$.ekit.isset(id)){
			return null;
		};
		force = $.ekit.initData(force, false);
		var old_id = $(this).attr('id');
		if(($.ekit.isset(old_id) && force == true) || !$.ekit.isset(old_id) || old_id == ""){
			$(this).attr('id', id);
			return id;
		};
		return old_id;
	};	
	///////////////////////////////////////
	///////////////////////////////////////
	///////////////////////////////////////
	//ekit specific variables
	///////////////////////////////////////
	///////////////////////////////////////
	///////////////////////////////////////
	$.ekit = {
		///////////////////////////////////
		app: {
			data: {},
			vars: {},
			get: function(key){
				if($.ekit.isset($.ekit.app.data[key])){
					return $.ekit.app.data[key];
				};
				return null;
			},
			set: function(key, value){				
				if($.ekit.isset($.ekit.app.data[key])){
					$.ekit.debug('app_key < '+key+' > has already assigned. Please check.');	
					return false;
				};
				$.ekit.app.data[key] = value;
				return true;
			}
		},
		///////////////////////////////////
		evar: {
			key: {
				template: null,
				index: 0,
				last: null
			},
			callback: []
		},
		///////////////////////////////////
		accordion_mouseover: function(){
			var cfg = ($.hoverintent = {
				sensitivity: 7,
				interval: 100
			});
			
			$.event.special.hoverintent = {
				setup: function() {
					$( this ).bind( "mouseover", jQuery.event.special.hoverintent.handler );
				},
				teardown: function() {
					$( this ).unbind( "mouseover", jQuery.event.special.hoverintent.handler );
				},
				handler: function( event ) {
					var that = this,
						args = arguments,
						target = $( event.target ),
						cX, cY, pX, pY;
			
					function track( event ) {
						cX = event.pageX;
						cY = event.pageY;
					};
					pX = event.pageX;
					pY = event.pageY;
					function clear() {
						target
							.unbind( "mousemove", track )
							.unbind( "mouseout", arguments.callee );
						clearTimeout( timeout );
					}
					function handler() {
						if ( ( Math.abs( pX - cX ) + Math.abs( pY - cY ) ) < cfg.sensitivity ) {
							clear();
							event.type = "hoverintent";
							// prevent accessing the original event since the new event
							// is fired asynchronously and the old event is no longer
							// usable (#6028)
							event.originalEvent = {};
							jQuery.event.handle.apply( that, args );
						} else {
							pX = cX;
							pY = cY;
							timeout = setTimeout( handler, cfg.interval );
						}
					}
					var timeout = setTimeout( handler, cfg.interval );
					target.mousemove( track ).mouseout( clear );
					return true;
				}
			};
		},
		///////////////////////////////////
		convertStringDate: function(value, from, to){
			//from = 'd/m/y'
			//to = y-m-d
			if(!$.ekit.isset(from)){
				from = 'd/m/y';	
			};
			if(!$.ekit.isset(to)){
				to = 'y-m-d';	
			};
			if(!$.ekit.isset(value)){
				return null;
			};
			from = from.toLowerCase();
			to = to.toLowerCase();
			//
			var tmp = {
				from: from,
				to: to
			};
			tmp.from = tmp.from.replace('d', '');
			tmp.from = tmp.from.replace('m', '');
			tmp.from = tmp.from.replace('y', '');
			tmp.from_s = tmp.from[0];
			tmp.from = from.split(tmp.from_s);
			tmp.value = value.split(tmp.from_s);
			var d = {};
			for(var i in tmp.from){
				if(tmp.from[i].indexOf('d') >= 0){
					d.d = tmp.value[i];
				};
				if(tmp.from[i].indexOf('m') >= 0){
					d.m = tmp.value[i];	
				};
				if(tmp.from[i].indexOf('y') >= 0){
					d.y = tmp.value[i];
				};
			};
			//to
			tmp.to = tmp.to.replace('d', '');
			tmp.to = tmp.to.replace('m', '');
			tmp.to = tmp.to.replace('y', '');
			tmp.to_s = tmp.to[0];
			tmp.to = to.split(tmp.to_s);
			//output
			var result = [];
			for(var i in tmp.to){
				result.push(d[tmp.to[i]]);
			}
			result = result.join(tmp.to_s);
			return result;
		},		
		///////////////////////////////////		
		convertHtmlObj: function(htmlObj, isUnique, parent, index){
			if(!$.ekit.isset(htmlObj)){
				return null;
			};
			if(!$.ekit.isset(isUnique)){
				isUnique = false;	
			};
			if(!$.ekit.isset(parent) || isUnique == true){
				parent = '';
			}
			if($.ekit.isset(index)){
				index = 0;	
			};
			//
			var maxIndex = 15;			
			if(index >= maxIndex){
				return null;	
			};
			//////////////
			var result = {};
			if(!$.ekit.isObject(htmlObj)){			
				htmlObj = {
					id: htmlObj	
				};
			};
			//
			var obj = '';
			if($.ekit.isset(htmlObj.custom)){
				obj = htmlObj.custom;
			};		
			if($.ekit.isset(htmlObj['class'])){
				obj = '.'+htmlObj['class'];
			};
			if($.ekit.isset(htmlObj['id'])){
				obj = "#"+htmlObj['id'];
			};
			//
			result = $$([parent, obj]);			
			parent = parent + ' ' + obj;
			result.me = parent;
			result.$ = {};
			for(var key in htmlObj){
				if(key == 'id' || key == 'class' || key == 'custom'){
					continue;
				};
				//
				result['$'+key] = result.$[key] = $.ekit.convertHtmlObj(htmlObj[key], isUnique, parent, index + 1);				
				/*continue;
				if($.ekit.isset($.fn[key])){
					result[key] = null;
				}else{
					result[key] = $.ekit.convertHtmlObj(htmlObj[key], isUnique, parent, index + 1);	
				}*/		
			}
			return result;
		},		
		///////////////////////////////////
		arrToCss: function(data){
			data = $.ekit.initData(data, {});
			var style = [];
			for(var i in data){
				style.push(i+':'+data[i]);
			};
			style = style.join(';');
			return style;
		},
		///////////////////////////////////
		debug: function(value, viewcode){
			if($.ekit.isObject(value)){
				var tmp = '';
				for(i in value){
					if(tmp != ''){
						tmp +=  '\r\n';	
					};
					tmp += i + ' => ' + value[i];
				};
				value = tmp;
			};
			var html = '<div class="_debug" style="position:fixed;top:150px;right:0px;width:300px;height:400px;background-color:#000000;color:#FFF;opacity:0.75;z-index:1000;overflow:scroll"><pre style="position:absolute; top:0px;bottom:0px;right:0px;left:0px; background-color:transparent;color:#FFFFFF; width:100%;height:100%"></pre><textarea class="no_tiny_mce" name="" cols="" rows="" style="position:absolute;top:0px;bottom:0px;right:0px;left:0px;background-color:transparent;color:#FFFFFF;width:100%;height:100%"></textarea></div>';
			if(!$("._debug").isExist()){
				$("body").append(html);
			};
			//viewcode
			viewcode = viewcode || false;
			$("._debug").children().each(function(){
				$(this).hide();
			});
			if(viewcode == true){
				//html = $("._debug textarea").attr("value") + "\n---------------------------------------------\n" + value;
				html = value + "\n-------\n" + $("._debug textarea").attr("value");
				$("._debug textarea").attr("value", html);
				$("._debug textarea")[0].scrollHeight;
				$("._debug textarea").show();			
			}else{
				//html = $("._debug div").html() + "<br />---------------------------------------------<br />" + value;
				html = value + "<br />-------<br />" + $("._debug pre").html();
				$("._debug pre").html(html);			
				$("._debug pre").show();
			};
		},
		///////////////////////////////////
		getIndex: function(){
			return $.ekit.evar.key.index++;
		},
		///////////////////////////////////
		getRandomKey: function(isLast){
			if(!$.ekit.isset(isLast)){
				isLast = false;
			};
			if(isLast == true && $.ekit.evar.key.last != null){
				return $.ekit.evar.key.last;
			};
			if(!$.ekit.isset($.ekit.evar.key.template)){
				var d = new Date();
				$.ekit.evar.key.template = d.getTime();
			};	
			var key = "__"+$.ekit.evar.key.template+"__"+$.ekit.getIndex();
			$.ekit.evar.key.last = key;
			return key;
		},
		///////////////////////////////////
		getCustomDate: function(custom, time, from, to){
			try{
				time = $.ekit.convertStringDate(time, from, 'Y-m-d');	
				var d = new Date(time);
				d = $.ekit.strtotime(custom, d.getTime() / 1000);
				d = new Date(d * 1000);
				d = d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();
				d = $.ekit.convertStringDate(d, 'Y-m-d', to);
				return d;
			}catch(ex){
				return time;	
			};
		},
		///////////////////////////////////
		getFirstDayOfMonth: function(value, from, to){
			if(!$.ekit.isset(from)){
				from = 'd/m/y';
			};
			if(!$.ekit.isset(to)){
				to = 'y-m-d';
			};
			from = from.toLowerCase();
			to = to.toLowerCase();
			value = $.ekit.convertStringDate(value, from, 'd/m/y');
			value = value.split('/');
			value[0] = 1;
			value = value.join('/');
			value = $.ekit.convertStringDate(value, 'd/m/y', to);
			return value;
		},
		getYear: function(value, from){
			if(!$.ekit.isset(from)){
				from = 'd/m/Y';
			};
			from = from.toLowerCase();
			value = $.ekit.convertStringDate(value, from, 'd/m/y');
			value = value.split('/');
			return value[2];
		},
		getMonth: function(value, from){
			if(!$.ekit.isset(from)){
				from = 'd/m/Y';
			};
			from = from.toLowerCase();
			value = $.ekit.convertStringDate(value, from, 'd/m/y');
			value = value.split('/');
			return value[1];
		},		
		getFirstMondayOfYear: function(year, format){
			if(!$.ekit.isset(format)){
				format = 'd/m/y';	
			};
			var d = new Date(year, 0, 1);
			var day = d.getDay();
			switch(day){
			case 0: //+1
				d = 1 + 1;		
				break;
			case 1:	//monday
				d = 1;
				break;
			default:
				d = 1 + 7 - (day - 1);
				break;
			};
			var value = [d, 1, year].join('/');
			value = $.ekit.convertStringDate(value, 'd/m/y', format);
			return value;
		},
		getFirstDayOfWeek: function(value, from, to){
			if(!$.ekit.isset(from)){
				from = 'd/m/y';	
			};
			if(!$.ekit.isset(to)){
				to = 'y-m-d';	
			};
			value = $.ekit.convertStringDate(value, from, 'd/m/y');
			value = value.split('/');
			value = new Date(value[2], value[1] - 1, value[0]);
			var d = value.getDay() - 1;
			if(d < 0){
				d += 7;
			};	
			value.setDate(value.getDate() - d);
			value = [value.getDate(), value.getMonth() + 1, value.getFullYear()].join('/');			
			value = $.ekit.convertStringDate(value, 'd/m/y', to);
			return value;
		},
		getWeek: function(value, from){			
			value = $.ekit.convertStringDate(value, from, 'd/m/y');
			value = value.split('/');
			//
			var onejan = $.ekit.getFirstMondayOfYear(value[2], 'd/m/y');
			onejan = onejan.split('/');
			onejan = new Date(onejan[2], onejan[1] - 1, onejan[0]);
			//
			var today = new Date(value[2], value[1] - 1, value[0]);
			var result = today - onejan;
			if(today.getDay() == 1){	//monday
				result += 1;
			};
			result = Math.ceil(result/86400000/7);
			return result;
		},
		///////////////////////////////////////
		//get hash
		getHash: function(index){
			var hash = window.location.hash;
			hash = hash.replace('#', '');
			hash = hash.split('/');			
			if($.ekit.isset(index)){
				return hash[index];
			}
			return hash;
		},
		///////////////////////////////////////
		//isset
		isset: function(val){
			if(val == undefined || val == null){
				return false;
			};
			return true;
		},
		//isObject
		isObject: function(obj){
			if(typeof obj == "object"){
				return true;
			};
			return false;
		},
		///////////////////////////////////////
		//setTimeout
		clearInterval: function(intervalID){
			return clearInterval(intervalID);
		},
		setInterval: function(func, delay, option){
			func = func || function(){};
			delay = delay || 240;
			option = option || {};
			return setInterval(function(){
				func.call(null, {delay:delay}, option);
			}, delay);
		},
		///////////////////////////////////////
		//setTimeout
		clearTimeout: function(timeoutID){
			return clearTimeout(timeoutID);
		},
		setTimeout: function(func, delay, option){
			func = func || function(){};
			delay = delay || 240;
			option = option || {};
			return setTimeout(function(){
				func.call(null, {delay:delay}, option);
			}, delay);
		},
		///////////////////////////////////
		initData: function(data, init_value){
			if(!$.ekit.isset(data)){	
				return init_value;
			};
			if(!$.ekit.isset(init_value)){
				return data;
			};
			if($.ekit.isObject(init_value)){
				if(!$.ekit.isObject(data)){
					data = {};
				};
				for(var i in init_value){
					data[i] = $.ekit.initData(data[i], init_value[i]);					
				};
			}else{
				if($.ekit.isObject(data)){
					data = null;
				};
				if(!$.ekit.isset(data)){
					data = init_value;
				};
			}		
			return data;
		},
		///////////////////////////////////
		loadModule: function(moduleName, container, option){
			$.ekit.ajax({
				url: 'ajax/def_load_module.php',
				type: 'post',
				data: {
					moduleName: moduleName,
					data: option.data
				},
				success: function(data){
					if(option.useContainer == true){
						data = '<div>'+data+'</div>';
					};
					$(container).append(data);
				}
			});
		},		
		///////////////////////////////////
		message: function(option){
			if(!$.ekit.isObject(option)){
				option = {
					message: option		
				};	
			};
			option = $.ekit.initData(option, {
				message: '',
				dialog: {}
			});
			if(option.message == ''){
				return;	
			};
			alert(option.message);
			return;
			var tmp = {
				modal: true,
				resizable: false,
				show: {
					effect: 'drop',
					direction: 'up',
					duration: 400
				},
				hide: {
					effect: 'drop',
					direction: 'up',
					duration: 200
				},
				draggable: false,
				closeOnEscape: true,
				width: '300px',
				height: '0px',
				buttons: {									
					'OK': function(){
						$(this).dialog('close');	
					}
				}
			};
			for(var i in option.dialog){
				tmp[i] = option.dialog[i];
			};
			$('<div title="'+option.message+'">').dialog(tmp);
		},
		///////////////////////////////////
		registerCallback: function(func, option){
			$.ekit.evar.callback.push({
				func: func,
				option: option	
			});
		},
		///////////////////////////////////
		strtotime: function(text, now){
			// Convert string representation of date and time to a timestamp  
			// 
			// version: 1109.2015
			// discuss at: http://phpjs.org/functions/strtotime
			// +   original by: Caio Ariede (http://caioariede.com)
			// +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
			// +      input by: David
			// +   improved by: Caio Ariede (http://caioariede.com)
			// +   improved by: Brett Zamir (http://brett-zamir.me)
			// +   bugfixed by: Wagner B. Soares
			// +   bugfixed by: Artur Tchernychev
			// +   improved by: A. Matías Quezada (http://amatiasq.com)
			// %        note 1: Examples all have a fixed timestamp to prevent tests to fail because of variable time(zones)
			// *     example 1: strtotime('+1 day', 1129633200);
			// *     returns 1: 1129719600
			// *     example 2: strtotime('+1 week 2 days 4 hours 2 seconds', 1129633200);
			// *     returns 2: 1130425202
			// *     example 3: strtotime('last month', 1129633200);
			// *     returns 3: 1127041200
			// *     example 4: strtotime('2009-05-04 08:30:00');
			// *     returns 4: 1241418600
			if (!text)
			  return null;
			
			// Unecessary spaces
			text = text.trim()
			  .replace(/\s{2,}/g, ' ')
			  .replace(/[\t\r\n]/g, '')
			  .toLowerCase();
			
			var parsed;
			
			if (text === 'now')
			  return now === null || isNaN(now) ? new Date().getTime() / 1000 | 0 : now | 0;
			else if (!isNaN(parse = Date.parse(text)))
			  return parse / 1000 | 0;
			if (text == 'now')
			  return new Date().getTime() / 1000; // Return seconds, not milli-seconds
			else if (!isNaN(parsed = Date.parse(text)))
			  return parsed / 1000;
			
			var match = text.match(/^(\d{2,4})-(\d{2})-(\d{2})(?:\s(\d{1,2}):(\d{2})(?::\d{2})?)?(?:\.(\d+)?)?$/);
			if (match) {
			  var year = match[1] >= 0 && match[1] <= 69 ? +match[1] + 2000 : match[1];
			  return new Date(year, parseInt(match[2], 10) - 1, match[3],
				  match[4] || 0, match[5] || 0, match[6] || 0, match[7] || 0) / 1000;
			};
			
			var date = now ? new Date(now * 1000) : new Date();
			var days = {
			  'sun': 0,
			  'mon': 1,
			  'tue': 2,
			  'wed': 3,
			  'thu': 4,
			  'fri': 5,
			  'sat': 6
			};
			var ranges = {
			  'yea': 'FullYear',
			  'mon': 'Month',
			  'day': 'Date',
			  'hou': 'Hours',
			  'min': 'Minutes',
			  'sec': 'Seconds'
			};
			
			function lastNext(type, range, modifier) {
			  var day = days[range];
			
			  if (typeof(day) !== 'undefined') {
				  var diff = day - date.getDay();
			
				  if (diff === 0)
					  diff = 7 * modifier;
				  else if (diff > 0 && type === 'last')
					  diff -= 7;
				  else if (diff < 0 && type === 'next')
					  diff += 7;
			
				  date.setDate(date.getDate() + diff);
			  };
			};
			function process(val) {
			  var split = val.split(' ');
			  var type = split[0];
			  var range = split[1].substring(0, 3);
			  var typeIsNumber = /\d+/.test(type);
			
			  var ago = split[2] === 'ago';
			  var num = (type === 'last' ? -1 : 1) * (ago ? -1 : 1);
			
			  if (typeIsNumber)
				  num *= parseInt(type, 10);
			
			  if (ranges.hasOwnProperty(range))
				  return date['set' + ranges[range]](date['get' + ranges[range]]() + num);
			  else if (range === 'wee')
				  return date.setDate(date.getDate() + (num * 7));
			
			  if (type === 'next' || type === 'last')
				  lastNext(type, range, num);
			  else if (!typeIsNumber)
				  return false;
			
			  return true;
			};
			
			var regex = '([+-]?\\d+\\s' +
			  '(years?|months?|weeks?|days?|hours?|min|minutes?|sec|seconds?' +
			  '|sun\\.?|sunday|mon\\.?|monday|tue\\.?|tuesday|wed\\.?|wednesday' +
			  '|thu\\.?|thursday|fri\\.?|friday|sat\\.?|saturday)|(last|next)\\s' +
			  '(years?|months?|weeks?|days?|hours?|min|minutes?|sec|seconds?' +
			  '|sun\\.?|sunday|mon\\.?|monday|tue\\.?|tuesday|wed\\.?|wednesday' +
			  '|thu\\.?|thursday|fri\\.?|friday|sat\\.?|saturday))(\\sago)?';
			
			match = text.match(new RegExp(regex, 'gi'));
			if (!match)
			  return false;
			
			for (var i = 0, len = match.length; i < len; i++)
			  if (!process(match[i]))
				  return false;
			
			// ECMAScript 5 only
			//if (!match.every(process))
			// return false;
			
			return (date.getTime() / 1000);
		},
		///////////////////////////////////
		submit: function(option){
			option = $.ekit.initData(option, {
				action: $(location).attr('href'),
				method: 'get',
				data: {}
			});
			var form = $('<form action="'+option.action+'" method="'+option.method+'">');
			var data = '';
			for(var i in option.data){
				$('<input name="'+i+'" value="'+option.data[i]+'" type="hidden">').appendTo(form);
			}
			form.submit();
		},
		///////////////////////////////////
		validUsername: function(username){
			var regexp = /^[a-z]([0-9a-z_])+$/i;	//Username may consist of a-z, 0-9, underscores, begin with a letter.
			if(regexp.test(username)){
				return true;
			}
			return false;
		},
		///////////////////////////////////
		validEmail: function(email){
			 // From jquery.validate.js (by joern), contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/
			var regexp = /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i;
			if(regexp.test(email)){
				return true;
			}
			return false;
		},
		///////////////////////////////////
		validPassword: function(password){
			var regexp = /^([0-9a-zA-Z])+$/;	//Password field only allow : a-z 0-9
			if(regexp.test(password)){
				return true;
			}
			return false;
		},
		///////////////////////////////////
		//Class
		///////////////////////////////////
		_Success: function(n, func, option){
			this.option = {
				n: 0,
				count: 0,
				func: function(){},
				option: {}
			};	
			this.option.n = n;
			this.option.func = func || function(){};
			this.option.option = option || {};
			
			this.success = function(){
				this.option.count++;
				if(this.option.count < this.option.n){
					return;	
				}
				this.option.func.call(this, {}, this.option.option);
			}	
		}
		///////////////////////////////////
	};
});

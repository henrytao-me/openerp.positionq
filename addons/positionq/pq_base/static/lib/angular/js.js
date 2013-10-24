var ngApp = angular.module('ngApp', []).directive('contenteditable', function() {
	return {
		require: 'ngModel',
		link: function(scope, elm, attrs, ctrl) {
			// view -> model
			elm.on('blur', function() {
				scope.$apply(function() {
					ctrl.$setViewValue(elm.html());
				});
			});

			elm.bind('keydown', function(e) {
				if(e.keyCode == 13) {
					e.preventDefault();
				}
			});

			// model -> view
			ctrl.$render = function(value) {
				elm.html(value);
			};

			// load init value from DOM
			ctrl.$setViewValue(elm.html());
		}
	};
}).directive('myRepeat', function($compile) {
	/*
	<th my-repeat="b in [1, 2]">
		<div my-repeat-elm="th">a {{b}}</div>
		<!-- <div my-repeat="tieu_chi in yeu_to.tieu_chi">
		<th colspan="1">{{tieu_chi.name}}</th>
		<th>Tổng điểm</th>
		<th>Mức độ</th>
		<th>Điểm công việc</th>
		</div> -->
	</th>
	 */
	
	var uid = ['0', '0', '0'];
	/*
	 * nextUid
	 */
	function nextUid() {
		var index = uid.length;
		var digit;

		while(index) {
			index--;
			digit = uid[index].charCodeAt(0);
			if(digit == 57 /*'9'*/) {
				uid[index] = 'A';
				return uid.join('');
			}
			if(digit == 90 /*'Z'*/) {
				uid[index] = '0';
			} else {
				uid[index] = String.fromCharCode(digit + 1);
				return uid.join('');
			}
		}
		uid.unshift('0');
		return uid.join('');
	};
	/*
	 * hashKey
	 */
	function hashKey(obj) {
		var objType = typeof obj, key;

		if(objType == 'object' && obj !== null) {
			if( typeof ( key = obj.$$hashKey) == 'function') {
				// must invoke on object to keep the right this
				key = obj.$$hashKey();
			} else if(key === undefined) {
				key = obj.$$hashKey = nextUid();
			}
		} else {
			key = obj;
		}

		return objType + ':' + key;
	};
	/*
	 * isArray
	 */
	function isArray(value) {
		return toString.apply(value) == '[object Array]';
	};
	/*
	 * HashQueueMap
	 */
	function HashQueueMap() {
	};
	HashQueueMap.prototype = {
		/*
		 * Same as array push, but using an array as the value for the hash
		 */
		push: function(key, value) {
			var array = this[ key = hashKey(key)];
			if(!array) {
				this[key] = [value];
			} else {
				array.push(value);
			}
		},

		/*
		 * Same as array shift, but using an array as the value for the hash
		 */
		shift: function(key) {
			var array = this[ key = hashKey(key)];
			if(array) {
				if(array.length == 1) {
					delete this[key];
					return array[0];
				} else {
					return array.shift();
				}
			}
		},

		/*
		 * return the first item without deleting it
		 */
		peek: function(key) {
			var array = this[hashKey(key)];
			if(array) {
				return array[0];
			}
		}
	};
	/*
	 *
	 * return
	 *
	 */
	return {
		transclude: 'element',
		compile: function(element, attr, linker) {
			return function(scope, iterStartElement, attr) {
				var expression = attr.myRepeat;
				var match = expression.match(/^\s*(.+)\s+in\s+(.*)\s*$/), lhs, rhs, valueIdent, keyIdent;
				if(!match) {
					throw Error("Expected myRepeat in form of '_item_ in _collection_' but got '" + expression + "'.");
				}
				lhs = match[1];
				rhs = match[2];
				match = lhs.match(/^(?:([\$\w]+)|\(([\$\w]+)\s*,\s*([\$\w]+)\))$/);
				if(!match) {
					throw Error("'item' in 'item in collection' should be identifier or (key, value) but got '" + lhs + "'.");
				}
				valueIdent = match[3] || match[1];
				keyIdent = match[2];

				// Store a list of elements from previous run. This is a hash where key is the
				// item from the
				// iterator, and the value is an array of objects with following properties.
				//   - scope: bound scope
				//   - element: previous element.
				//   - index: position
				// We need an array of these objects since the same object can be returned from
				// the iterator.
				// We expect this to be a rare case.
				var lastOrder = new HashQueueMap();

				scope.$watch(function myRepeatWatch(scope) {
					var index, length, collection = scope.$eval(rhs), cursor = iterStartElement, //
					// current position of the node
					// Same as lastOrder but it has the current state. It will become the
					// lastOrder on the next iteration.
					nextOrder = new HashQueueMap(), arrayBound, childScope, key, value, // key/value
					// of iteration
					array, last;
					// last object information {scope, element, index}

					if(!isArray(collection)) {
						// if object, extract keys, sort them and use to determine order of iteration
						// over obj props
						array = [];
						for(key in collection) {
							if(collection.hasOwnProperty(key) && key.charAt(0) != '$') {
								array.push(key);
							}
						}
						array.sort();
					} else {
						array = collection || [];
					}

					arrayBound = array.length - 1;

					// we are not using forEach for perf reasons (trying to avoid #call)
					for( index = 0, length = array.length; index < length; index++) {

						key = (collection === array) ? index : array[index];
						value = collection[key];

						last = lastOrder.shift(value);

						if(last) {
							// if we have already seen this object, then we need to reuse the
							// associated scope/element
							childScope = last.scope;
							nextOrder.push(value, last);

							if(index === last.index) {
								// do nothing
								cursor = last.element;
							} else {
								// existing item which got moved
								last.index = index;
								// This may be a noop, if the element is next, but I don't know of a good way to
								// figure this out,  since it would require extra DOM access, so let's just hope
								// that
								// the browsers realizes that it is noop, and treats it as such.
								cursor.after(last.element);
								cursor = last.element;
							}
						} else {
							// new item which we don't know about
							childScope = scope.$new();
						}

						childScope[valueIdent] = value;
						if(keyIdent)
							childScope[keyIdent] = key;
						childScope.$index = index;

						childScope.$first = (index === 0);
						childScope.$last = (index === arrayBound);
						childScope.$middle = !(childScope.$first || childScope.$last);

						/*
						 * upgrade ng-repeat
						 */
						try {
							var maxLevel = 5;
							for(var ii = maxLevel; ii > 0; ii--){
								var kk = '';
								for(var jj = 0; jj < ii; jj++){
									kk += '*[my-repeat] ';
								};
								last.element.find(kk).each(function() {
									$(this).children().each(function(){
										var elm = $(this).attr('my-repeat-elm');
										if(elm){
											var newObj = $('<'+elm+'>').append($(this).html());
											var attr = $(this).attr('my-repeat-attr') || '';
											attr = attr.split(',');
											for(i in attr){
												newObj.attr(attr[i], $(this).attr(attr[i]));
											};
											$(this).replaceWith(newObj);
										};
									});
									$(this).replaceWith($(this).html());
								});	
							};
							last.element.children().each(function(){
								var elm = $(this).attr('my-repeat-elm');
								if(elm){
									var newObj = $('<'+elm+'>').append($(this).html());
									var attr = $(this).attr('my-repeat-attr') || '';
									attr = attr.split(',');
									for(i in attr){
										newObj.attr(attr[i], $(this).attr(attr[i]));
									};
									$(this).replaceWith(newObj);
								};
							});
							last.element.replaceWith(last.element.html());
						} catch(ex) {
						};
						/*
						 * end upgrade
						 */

						if(!last) {
							linker(childScope, function(clone) {
								cursor.after(clone);
								last = {
									scope: childScope,
									element: ( cursor = clone),
									index: index
								};
								nextOrder.push(value, last);
							});
						};
					};

					//shrink children
					for(key in lastOrder) {
						if(lastOrder.hasOwnProperty(key)) {
							array = lastOrder[key];
							while(array.length) {
								value = array.pop();
								value.element.remove();
								value.scope.$destroy();
							};
						};
					};
					lastOrder = nextOrder;
				});
			};
		}
	}
});

// 'improve' Math.round() to support a second argument
var _round = Math.round;
Math.round = function(number, decimals /* optional, default 0 */) {
	if(arguments.length == 1)
		return _round(number);

	var multiplier = Math.pow(10, decimals);
	return _round(number * multiplier) / multiplier;
};

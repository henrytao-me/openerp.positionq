/* fix openerp bug: unsupport bind function in some devices (Ex: ipad, iphone...)
 * Ref bind function: 
 * https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/Function/bind
 * http://www.bennadel.com/blog/1517-Binding-Javascript-Method-References-To-Their-Parent-Classes.htm
 * check bug in:
 * chrome.js - instance.web.Client - init function
 * corelib.js - instance.web.Widget - init function - this[name] = this[name].bind(this); 
 */
if (!Function.prototype.bind) {
  Function.prototype.bind = function (oThis) {
    if (typeof this !== "function") {
      // closest thing possible to the ECMAScript 5 internal IsCallable function
      throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");
    }
 
    var aArgs = Array.prototype.slice.call(arguments, 1), 
        fToBind = this, 
        fNOP = function () {},
        fBound = function () {
          return fToBind.apply(this instanceof fNOP && oThis
                                 ? this
                                 : oThis,
                               aArgs.concat(Array.prototype.slice.call(arguments)));
        };
 
    fNOP.prototype = this.prototype;
    fBound.prototype = new fNOP();
 
    return fBound;
  };
};
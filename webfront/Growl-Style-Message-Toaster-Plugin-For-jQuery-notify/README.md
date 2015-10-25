jQuery.notify 1.0
================

jQuery.notify is a jQuery plugin that makes it easy to create alert - success - error - warning - information messages as an alternative the standard alert dialog.

__<a href="http://creativedream.net/plugins/jquery.notify/" target="_blank">Demo Page</a>__

Usage
-------
__Styles:__

Include the jquery.notify css file in your html page.
~~~~ html
<link href="jquery.notify.css" type="text/css" rel="stylesheet" />
~~~~
__Javascript:__

Include the jQuery library and jquery.notify script file in your html page.
~~~~ html
<script src="http://code.jquery.com/jquery-latest.min.js"></script>
<script src="jquery.notify.min.js"></script>
~~~~

The function is called 'notify'. So just call it ;)
~~~ javascript
notify({
	type: "alert", //alert | success | error | warning | info
	title: "jQuery.Notify",
	message: "Super simple Notify plugin.",
	position: {
	    x: "right", //right | left | center
	    y: "top" //top | bottom | center
	},
	icon: '<img src="images/paper_plane.png" />', //<i>, <img>
	size: "normal", //normal | full | small
	overlay: false, //true | false
	closeBtn: true, //true | false
	overflowHide: false, //true | false
	spacing: 20, //number px
	theme: "default", //default | dark-theme
	autoHide: true, //true | false
	delay: 2500, //number ms
	onShow: null, //function
	onClick: null, //function
	onHide: null, //function
	template: '<div class="notify"><div class="notify-text"></div></div>'
});
~~~~

License
-------
> Licensed under <a href="http://opensource.org/licenses/MIT">MIT license</a>.

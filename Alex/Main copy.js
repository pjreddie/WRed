/*!
 * Ext JS Library 3.2.1
 * Copyright(c) 2006-2010 Ext JS, Inc.
 * licensing@extjs.com
 * http://www.extjs.com/license
 */
Ext.onReady(function(){

    var orientationChild = {
	frame = true;
	width: 200,
	html: 'Hi there',
	title: 'child 1'
    }

    var resultsChild = {
	width: 200,
	html: '#2',
	title: 'child 2'
    }
    var myWin = new Ext.Window({
	height: 300,
	width: 400,
	title: 'A test window',
	autoScroll: true,
	items: [
	    orientationChild,
	    resultsChild
	]
    }


    var p = new Ext.Panel({
        title: 'Four Circle Diffractometer Calculator',
        collapsible: false,
        renderTo: 'panel-basic',
        width: 400,
	height: 300,
        html: 'TESTING!'
	/*items: [
	   orientationChild,
	   resultsChild
	],*/
	//p.doLayout();
    });


});



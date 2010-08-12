/*
 * Author: Alex Yee
 *
 * Edit History:
 * 7/12/2010: Created and completed. Created layout, columns, and data sending/receiving/updating. 
 *             Not entirely beautified yet.
 * 7/13/2010: Restructured to give each numberfield (of input) a separate variable so I could
 *             send their given values to the backend for calculations.
 */

Ext.onReady(function () {
    var conn = new Ext.data.Connection();
    var isUBcalculated = 'no';     //Tells whether UB matrix has been calculated
                                   //either: 'no', 'yes', or 'refined'
                                   
// ********* START - Defining and assigning variables for the numberfield inputs  *********
    var aField = new Ext.form.NumberField({
        fieldLabel: 'a',
        allowBlank: false,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var bField = new Ext.form.NumberField({
        fieldLabel: 'b',
        allowBlank: false,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var cField = new Ext.form.NumberField({
        fieldLabel: 'c',
        allowBlank: false,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var alphaField = new Ext.form.NumberField({
        fieldLabel: 'α',
        allowBlank: false,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var betaField = new Ext.form.NumberField({
        fieldLabel: 'β',
        allowBlank: false,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var gammaField = new Ext.form.NumberField({
        fieldLabel: 'γ',
        allowBlank: false,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var wavelengthField = new Ext.form.NumberField({
        fieldLabel: 'Wavelength (λ)',
        allowBlank: true,
        decimalPrecision: 7
    });
    
    
    //scattering plane h, k, l numberfields:
    var h1Field = new Ext.form.NumberField({
        fieldLabel: 'h1',
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var k1Field = new Ext.form.NumberField({
        fieldLabel: 'k1',
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var l1Field = new Ext.form.NumberField({
        fieldLabel: 'l1',
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var h2Field = new Ext.form.NumberField({
        fieldLabel: 'h2',
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var k2Field = new Ext.form.NumberField({
        fieldLabel: 'k2',
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-10'
    });
    var l2Field = new Ext.form.NumberField({
        fieldLabel: 'l2',
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-10'
    });
    
    //UB matrix numberfields:
    var UB11Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB12Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB13Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB21Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB22Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB23Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB31Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB32Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    var UB33Field = new Ext.form.NumberField({
        allowBlank: true,
        decimalPrecision: 7,
        anchor: '-3'
    });
    
    //phi fixed phi field
    var phiField = new Ext.form.NumberField({
        fieldLabel: 'Fixed Phi (φ)',
        allowBlank: false,
        decimalPrecision: 7,
    });
    
    // ********* END - Defining and assigning variables for the numberfield inputs  *********  
                                   
    myUBmatrix = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] //The variable that will hold the calculated UB matrix

    var baseData = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    ];
    var baseIdealData = [
        [0.0, 0.0, 0.0, '0.0', '0.0', '0.0', '0.0', '0.0'],
    ];

    // create the Data Store
    var UBInputFields = [
        { name: 'h',        type: 'float'},
        { name: 'k',        type: 'float'},
        { name: 'l',        type: 'float'},
        { name: 'twotheta', type: 'float'},
        { name: 'theta',    type: 'float'},
        { name: 'chi',      type: 'float'},
        { name: 'phi',      type: 'float'},
    ] 
    var store = new Ext.data.ArrayStore({
        autodestroy     : false,
        storeId         : 'UBInputStore',
        fields          : UBInputFields
    });
    store.loadData(baseData);
    
    
    var desiredFields = [
        { name: 'h'},
        { name: 'k'},
        { name: 'l'},
        { name: 'twotheta'},
        { name: 'theta'},
        { name: 'omega'},
        { name: 'chi'},
        { name: 'phi'},
    ] 
    var idealDataStore = new Ext.data.ArrayStore({
        autoDestroy     : false,
        storeId         : 'desiredStore',
        fields          : desiredFields
    });
    idealDataStore.loadData(baseIdealData);
    
    
    // ********* START - Creating Column Models *********
    var numberFieldEditor = new Ext.form.NumberField({
        allowBlank: false,
        allowDecimals: true,
        decimalPrecision: 7
    });
    var textFieldEditor = new Ext.form.TextField({
        maxLength: 11,
    });

    var cm = new Ext.grid.ColumnModel({
        // specify any defaults for each column
        defaults: {
            sortable: false,
            align: 'right',
            width: 60,     
            editor: new Ext.form.NumberField({
                allowBlank: false,
                allowDecimals: true,
                decimalPrecision: 7 
            })
        },
        columns: [
            {
            header: 'h',
            dataIndex: 'h'
            },
        {
            header: 'k',
            dataIndex: 'k'
            },
        {
            header: 'l',
            dataIndex: 'l'
            },
        {
            header: '2θ',
            dataIndex: 'twotheta'
            },
        {
            header: 'θ',
            dataIndex: 'theta'
            },
        {
            header: 'χ',
            dataIndex: 'chi'
            },
        {
            header: 'φ',
            dataIndex: 'phi'
            },
        ]
    });
    
    var cm2 = new Ext.grid.ColumnModel({
        defaults: {
            sortable: false,
            align: 'right',
            width: 65,
            /*editor: new Ext.form.NumberField({
                allowBlank: false,
                allowDecimals: true,
                decimalPrecision: 7
            })*/
        },
        columns: [
        {
            header: 'h',
            dataIndex: 'h',
            editor: numberFieldEditor
        }, {
            header: 'k',
            dataIndex: 'k',
            editor: numberFieldEditor
        }, {
            header: 'l',
            dataIndex: 'l',
            editor: numberFieldEditor
        }, {
            header: '2θ',
            dataIndex: 'twotheta',
            editor: textFieldEditor
        }, {
            header: 'θ',
            dataIndex: 'theta',
            editor: textFieldEditor
        }, {
            header: 'ω',
            dataIndex: 'omega',
            editor: textFieldEditor
        }, {
            header: 'χ',
            dataIndex: 'chi',
            editor: textFieldEditor
        }, {
            header: 'φ',
            dataIndex: 'phi',
            editor: textFieldEditor
        },
        ]
    });
    
    //Setting the calculated angle values to uneditable
    cm2.setEditable(3, false);
    cm2.setEditable(4, false);
    cm2.setEditable(5, false);
    cm2.setEditable(6, false);
    cm2.setEditable(7, false);
    // ********* END - Creating Column Models *********
    
    // create the editor grids
    var observationGrid = new Ext.grid.EditorGridPanel({
        store: store,
        cm: cm,
        id              : 'observationEditorGrid',
        width           : 440,
        height          : 187,
        title           : 'Observations',
        frame           : true,
        clicksToEdit    : 1,
        decimalPrecision: 6, //still showing 7 decimal places...
        viewConfig: { 
            forceFit : true
        },
        bbar: [{
            text: 'Add New Row',
            handler: addRowObservation
        }, 
        '-', //Shorthand for Ext.Tollbar.Separator (the " | " between buttons)
        {
            text: 'Calculate UB Matrix',
            handler: submitData
        },
        '-',
        {
            text: 'Refine UB Matrix',
            handler: RefineSubmitData
        },
        '-',
        {
            text: 'Evaluate Lattice',
            handler: getLattice
        }]
        
    });
    
    var grid2 = new Ext.grid.EditorGridPanel({
        store: idealDataStore,
        cm: cm2,
        width: 539,
        height: 200,
        title: 'Desired Results',
        frame: true,
        clicksToEdit: 1,        
        decimalPrecision: 6,
        tbar: [{
            text: 'Add New Row',
            handler: addRow
        }, 
        '-',  
        {
            text: '*** CALCULATE RESULTS ***',
            handler: calculateResults
        }]
    });
    
    // ****************** START - Defining grid button functions ****************** 
    function submitData(button, event) { 
        //Calculates and stores the B and UB matricies when the button 'Calculate UB Matrix' is pressed
        params = {'data': [] };
        
        //only sends the first two row's of observations
        for (var i = 0; i < 2; i++) {
            var record = store.getAt(i)
            params['data'].push(record.data); 
        };
        
        params['data'].push({
            'a': aField.getValue(),
            'b': bField.getValue(),
            'c': cField.getValue(),
            'alpha': alphaField.getValue(),
            'beta': betaField.getValue(),
            'gamma': gammaField.getValue()
        });

        conn.request({
            url: '/WRed/files/calcUBmatrix/',
            method: 'POST',
            params: Ext.encode(params),
            success: ubsuccess,
            failure: function () {
                isUBcalculated = 'no';
                Ext.Msg.alert('Error: Failed to calculate UB matrix');
            }
        });

    };
    
    function RefineSubmitData (button, event) { 
        //Calculates and stores the B and UB matricies when the button 'Refine UB Matrix' is pressed
        params = {'data': [] };

        params['data'].push({
            'wavelength': wavelengthField.getValue()
        });

        for (var i = 0; i < store.getCount(); i++) {
            var record = store.getAt(i)            
            //there will never be a (0,0,0) h,k,l vector so don't push that row
            if (record.data['h'] != 0 || record.data['k'] != 0 || record.data['l'] != 0){   
                params['data'].push(record.data); //adding table's input to data to be sent to backend
            }
        };
        
        conn.request({
            url: '/WRed/files/refineUBmatrix/',
            method: 'POST',
            params: Ext.encode(params),
            success: refineubsuccess,
            failure: function () {
                isUBcalculated = 'no';
                Ext.Msg.alert('Error: Failed to calculate UB matrix');
            }
        });
    };
    
    function ubsuccess (responseObject) {
        stringUBmatrix = responseObject.responseText; //Receives UBmatrix as a String w/ elements separated by a ', '
        myUBmatrix = stringUBmatrix.split(', '); //Makes a 1D array of the 9 UBmatrix values, each as a String
        for (i = 0; i < 9 ; i++){
            myUBmatrix[i] = parseFloat(myUBmatrix[i]); //Converts each String into a Float
        }
        
        //displaying UB matrix values
        UB11Field.setValue(myUBmatrix[0]);
        UB12Field.setValue(myUBmatrix[1]);
        UB13Field.setValue(myUBmatrix[2]);
        UB21Field.setValue(myUBmatrix[3]);
        UB22Field.setValue(myUBmatrix[4]);
        UB23Field.setValue(myUBmatrix[5]);
        UB31Field.setValue(myUBmatrix[6]);
        UB32Field.setValue(myUBmatrix[7]);
        UB33Field.setValue(myUBmatrix[8]);

        isUBcalculated = 'yes';
        store.commitChanges(); //removes red mark in corner of cell that indicates an uncommited edit
    };
    

    function refineubsuccess (responseObject) {
        //TODO may need to add in calculated lattice parameters
    
        stringUBmatrix = responseObject.responseText; //Receives UBmatrix as a String w/ elements separated by a ', '
        myUBmatrix = stringUBmatrix.split(', '); //Makes a 1D array of the 9 UBmatrix values, each as a String
        for (i = 0; i < 9 ; i++){
            myUBmatrix[i] = parseFloat(myUBmatrix[i]); //Converts each String into a Float
        }
        
        //displaying UB matrix values
        UB11Field.setValue(myUBmatrix[0]);
        UB12Field.setValue(myUBmatrix[1]);
        UB13Field.setValue(myUBmatrix[2]);
        UB21Field.setValue(myUBmatrix[3]);
        UB22Field.setValue(myUBmatrix[4]);
        UB23Field.setValue(myUBmatrix[5]);
        UB31Field.setValue(myUBmatrix[6]);
        UB32Field.setValue(myUBmatrix[7]);
        UB33Field.setValue(myUBmatrix[8]);

        isUBcalculated = 'refined';
        store.commitChanges(); 
    };
    
    
    function calculateResults(button, event) {
        //Calculates the desired angles when the button 'Calculate Results' is pressed
        params = {'data': [] };
        
        //IF the combobox is in the Bisecting Plane mode
        if (myCombo.getValue() == 'Bisecting'){

            //sending back all necessary data to calculate UB and desired angles
            params['data'].push({
                'a'         : aField.getValue(),
                'b'         : bField.getValue(),
                'c'         : cField.getValue(),
                'alpha'     : alphaField.getValue(),
                'beta'      : betaField.getValue(),
                'gamma'     : gammaField.getValue(),
                'wavelength': wavelengthField.getValue(),
                'UBmatrix'  : myUBmatrix
            }); 

            for (var j = 0; j < idealDataStore.getCount(); j++){
                //gets all the data from the Desired Data table
                var record = idealDataStore.getAt(j);
                params['data'].push(record.data);
            }  
                
            conn.request({
                url: '/WRed/files/omegaZero/',
                method: 'POST',
                params: Ext.encode(params),
                success: successFunction,
                failure: function () {
                    Ext.Msg.alert('Error: Failed calculation for Bisecting mode');
                }
            });
        }
 
        //ELSE IF the combobox is in the Scattering Plane mode
        else if (myCombo.getValue() == 'Scattering Plane'){
            
            //sending back all necessary data to calculate UB and desired angles
            params['data'].push({
                'a'         : aField.getValue(),
                'b'         : bField.getValue(),
                'c'         : cField.getValue(),
                'alpha'     : alphaField.getValue(),
                'beta'      : betaField.getValue(),
                'gamma'     : gammaField.getValue(),
                'h1'        : h1Field.getValue(),
                'k1'        : k1Field.getValue(),
                'l1'        : l1Field.getValue(),
                'wavelength': wavelengthField.getValue(),
                'h2'        : h2Field.getValue(),
                'k2'        : k2Field.getValue(),
                'l2'        : l2Field.getValue(),
                'UBmatrix'  : UBmatrix
            });

            for (var j = 0; j < idealDataStore.getCount(); j++){
                var record = idealDataStore.getAt(j)
                params['data'].push(record.data);
            }

            conn.request({
                url: '/WRed/files/scatteringPlane/',
                method: 'POST',
                params: Ext.encode(params),
                success: successFunction,
                failure: function () {
                    Ext.Msg.alert('Error: Failed calculation for Scattering Plane mode');
                }
            });
        }
        else if (myCombo.getValue() == 'Phi Fixed'){
            
            //sending back all necessary data to calculate UB and desired angles
            params['data'].push({
                'a'         : aField.getValue(),
                'b'         : bField.getValue(),
                'c'         : cField.getValue(),
                'alpha'     : alphaField.getValue(),
                'beta'      : betaField.getValue(),
                'gamma'     : gammaField.getValue(),
                'wavelength': wavelengthField.getValue(),
                'phi'       : phiField.getValue(),
                'UBmatrix'  : UBmatrix
            });
            
            for (var j = 0; j < idealDataStore.getCount(); j++){
                var record = idealDataStore.getAt(j);
                params['data'].push(record.data);
            }

            conn.request({
                url: '/WRed/files/phiFixed/',
                method: 'POST',
                params: Ext.encode(params),
                success: successFunction,
                failure: function () {
                    Ext.Msg.alert('Error: Failed calculation for Phi Fixed mode');
                }
            });
        }
        else {
            Ext.Msg.alert('Error: Please select a valid calculation mode');
        }
    };
    
    function successFunction(responseObject) {
        idealdata = Ext.decode(responseObject.responseText);
        
        //Updating desired data table
        changes = ['twotheta', 'theta', 'omega', 'chi', 'phi'];
        for (var i = 0; i < idealDataStore.getCount(); i++){
            record = idealDataStore.getAt(i); 
            if (idealdata[i] == 'Error') {
                //setting up the error message
                record.set('twotheta', 'Invalid');
                record.set('theta', 'Vector!');
                record.set('omega', 'Not in');
                record.set('chi', 'Scattering');
                record.set('phi', 'Plane.');
            }
            else{
                for (var c in changes) {
                    fieldName = changes[c];
                    record.set(fieldName, idealdata[i][fieldName]);
                }
            }
        }
        
        idealDataStore.commitChanges();
    }

    
    function addRowObservation() {
        var input = observationGrid.getStore().recordType;
        var r = new input({
            h: 0.0,
            k: 0.0,
            l: 0.0,
            twotheta: 0.0,
            theta: 0.0,
            omega: 0.0,
            chi: 0.0,
            phi: 0.0
        });
        observationGrid.stopEditing(); 
        store.add(r); //adds new row to the bottom of the table (ie the last row)
        observationGrid.startEditing(store.getCount()-1, 0); //starts editing for first cell of new row
    };
    
    function addRow() {
        var input = grid2.getStore().recordType;
        var r = new input({
            h: 0.0,
            k: 0.0,
            l: 0.0,
            twotheta: 0.0,
            theta: 0.0,
            omega: 0.0,
            chi: 0.0,
            phi: 0.0
        });
        grid2.stopEditing(); 
        idealDataStore.add(r); //adds new row to the bottom of the table (ie the last row)
        grid2.startEditing(idealDataStore.getCount()-1, 0); //starts editing for first cell of new row
    };
    
    function getLattice() {
        //With a calculated UB matrix, the lattice parameters can be calculated
        
        params = {'UBmatrix': myUBmatrix};

        conn.request({
            url: '/WRed/files/latticeParameters/',
            method: 'POST',
            params: Ext.encode(params),
            success: displayLattice,
            failure: function () {
                Ext.Msg.alert('Error: Could not calculate the lattice parameters from the UB matrix');
            }
        });
    };
    
    function displayLattice (responseObject){
        //console.log(responseObject);
        lattice = Ext.decode(responseObject.responseText);
        //console.log(lattice);
        
        aField.setValue(lattice['a']);
        bField.setValue(lattice['b']);
        cField.setValue(lattice['c']);
        alphaField.setValue(lattice['alpha']);
        betaField.setValue(lattice['beta']);
        gammaField.setValue(lattice['gamma']);
    }
    
    // ****************** END - Defining grid button functions ****************** 
   

    // ********* START - Setting up lattice constants GUI  ********* 
    var topFieldset = {
        xtype       : 'fieldset',
        border      : false,
        defaultType : 'numberfield',
        defaults    : {
            allowBlank : false,
            decimalPrecision: 10
        },
        items: [
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '115%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items   : [
                            aField
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items       : [
                            bField                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items       : [
                            cField                               
                        ]
                    }, {
                        //Buffer blank space to even out the c inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items   : [
                            alphaField
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items       : [
                            betaField                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 10,
                        items       : [
                            gammaField                               
                        ]
                    }, {
                        //Buffer blank space to even out the gamma inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            wavelengthField,
        ]
    };
    // ********* END - Setting up lattice constants GUI  ********* 

    
    // ********* START - Setting up scattering plane h/k/l GUI  ********* 
    var ScatteringFieldset = {
        xtype       : 'fieldset',
        border      : false,
        defaultType : 'numberfield',
        defaults    : {
            allowBlank : false,
            decimalPrecision: 10
        },
        items: [
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 15,
                        items   : [
                            h1Field
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 15,
                        items       : [
                            k1Field                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 15,
                        items       : [
                            l1Field                               
                        ]
                    }, {
                        //Buffer blank space to even out the l1 inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 15,
                        items   : [
                            h2Field
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 15,
                        items       : [
                            k2Field                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 100,
                        labelWidth  : 15,
                        items       : [
                            l2Field                               
                        ]
                    }, {
                        //Buffer blank space to even out the l2 inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            {
                //empty container to allow horizontal inputboxes for h,k,l
                xtype       : 'container',
                border      : false,
                width       : 230
            } 
        ]
    };
    
    // ********* END - Setting up scattering plane h/k/l GUI  ********* 
    
    // ********* START - Setting up phi fixed GUI  ********* 
    var PhiFixedFieldset = {
        xtype       : 'fieldset',
        border      : false,
        defaultType : 'numberfield',
        defaults    : {
            allowBlank : false,
            decimalPrecision: 10
        },
        items: [
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 250,
                        labelWidth  : 80,
                        items   : [
                            phiField
                        ]
                    },
                    {
                        //Buffer blank space to even out the phi inputbox
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            }
        ]
    };
    
    // ********* END - Setting up phi fixed GUI  ********* 
    
    
    // ********* START - Setting up calculated UB matrix GUI  ********* 
    var UBFieldset = {
        xtype       : 'fieldset',
        title       : 'UB Matrix',
        border      : false,
        defaultType : 'numberfield',
        defaults    : {
            allowBlank : true,
            decimalPrecision: 7
        },
        items: [
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items   : [
                            UB11Field
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items       : [
                            UB12Field                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items       : [
                            UB13Field                               
                        ]
                    }, {
                        //Buffer blank space to even out the first row of numberfields
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items   : [
                             UB21Field
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items       : [
                            UB22Field                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items       : [
                            UB23Field                               
                        ]
                    }, {
                        //Buffer blank space to even out the second row of numberfields
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            {
                xtype       : 'container',
                border      : false,
                layout      : 'column',
                anchor      : '100%',
                items       : [
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items   : [
                             UB31Field
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items       : [
                            UB32Field                               
                        ]
                    },
                    {
                        xtype       : 'container',
                        layout      : 'form',
                        width       : 75,
                        labelWidth  : 1,
                        items       : [
                            UB33Field                               
                        ]
                    }, {
                        //Buffer blank space to even out the third row of numberfields
                        xtype       : 'container',
                        layout      : 'form',
                        columnWidth : 1,
                        labelWidth  : 1
                    }
                ]
            },
            {
                //empty container to allow a 3x3 arrangement of numberfields for the UB matrix
                xtype       : 'container',
                border      : false,
                width       : 230
            }
        ]
    };
    
    // ********* END - Setting up calculated UB matrix GUI  ********* 
    
    // ********* START - Handling loading and saving data  ********* 
    
    var uploadPanel = new Ext.FormPanel({
        fileUpload: true,
        frame: true,
        title: 'Upload A Data File',
        autoHeight: true,
        bodyStyle: 'padding: 0 10px 5px 10px;',
        labelWidth: 30,
        items: [{
            xtype       : 'fileuploadfield',
            anchor      : '100%',
            id          : 'inputfile',
            emptyText   : 'Select a file...',
            fieldLabel  : 'File',
            name        : 'file',
            buttonText  : 'Browse...'
        }],
        buttons: [{
            text: 'Save & Download Data', //Save & Download Data button
            icon: '/media/icons/silk/disk.png', //graphic that accompanies the button
            handler: saveFunction
        }, {
            text: 'Load Data',  //Load Data button
            icon: '/media/icons/silk/add.png',
            handler: function (){
                if (uploadPanel.getForm().isValid()) {
                    uploadPanel.getForm().submit({
                        url: '/WRed/files/uploadingData/',
                        waitMsg: 'Uploading data...',
                        method: 'POST',
                        success: uploadFunction,
                        failure: function() {
                            Ext.Msg.alert('Error: Could not upload data.');
                        }
                    })
                }
                else {
                    Ext.Msg.alert('Error: Could not upload data.');
                }
            }
        }]
    });
    
    function saveFunction() {
        //Writes data to a textfile for user to download
        
        params = {'data': [] };

        params['data'].push({
            'h1'        : h1Field.getValue(), //h, k, ls are the scattering plane vectors
            'k1'        : k1Field.getValue(),
            'l1'        : l1Field.getValue(),
            'wavelength': wavelengthField.getValue(),
            'h2'        : h2Field.getValue(),
            'k2'        : k2Field.getValue(),
            'l2'        : l2Field.getValue(),        
            'a'         : aField.getValue(),
            'b'         : bField.getValue(),
            'c'         : cField.getValue(),
            'alpha'     : alphaField.getValue(),
            'beta'      : betaField.getValue(),
            'gamma'     : gammaField.getValue(),
            'mode'      : myCombo.getValue(),
            'numrows'   : store.getCount(),
            'ub'        : myUBmatrix,
            'phi'       : phiField.getValue(),
            'isUBcalculated': isUBcalculated
        });
        for (var i = 0; i < store.getCount(); i++) { //all the observation table's data 
            var record1 = store.getAt(i)
            params['data'].push(record1.data); 
        }; 
        for (var j = 0; j < idealDataStore.getCount(); j++){ //all the desired results table's data
            var record2 = idealDataStore.getAt(j)
            params['data'].push(record2.data);
        }  
            
        conn.request({
            url: '/WRed/files/savingData/',
            method: 'POST', 
            params: Ext.encode(params),
            success: function (){
                window.open('/WRed/files/downloadingData/'); //opens dialogue box window
            },
            failure: function () {
                Ext.Msg.alert('Error: Could not save');
            }
        });
        
    };
    
    
    
    function uploadFunction (formPanel, uploadObject) {
        responseJSON = Ext.decode(uploadObject.response.responseText);
        data = responseJSON['data']['array'];
        
        if (data[0] == null){
            Ext.Msg.alert('Error: Please select a file.');
        }
        else{
            //uploading lattice constants data
            aField.setValue(data[0]['a']);
            bField.setValue(data[0]['b']);
            cField.setValue(data[0]['c']);
            alphaField.setValue(data[0]['alpha']);
            betaField.setValue(data[0]['beta']);
            gammaField.setValue(data[0]['gamma']);
            wavelengthField.setValue(data[0]['wavelength']);
            
            //uploading comboBox (mode) information
            myCombo.setValue(data[0]['mode']);
            valueObject = {'data': {'mode': data[0]['mode']}};
            comboFunction(myCombo, valueObject);
            
            //uploading scattering plane vectors
            h1Field.setValue(data[0]['h1']);
            k1Field.setValue(data[0]['k1']);
            l1Field.setValue(data[0]['l1']);
            h2Field.setValue(data[0]['h2']);
            k2Field.setValue(data[0]['k2']);
            l2Field.setValue(data[0]['l2']);
            
            //uploading fixed phi value
            phiField.setValue(data[0]['phi']);
            
            //uploading observation data and ideal data
            newData = [];
            newIdealData = [];
            for (i = 1; i < data.length; i++){
                if (data[i]['omega'] == null){ //omega = null if it's observation data
                    tempData = [data[i]['h'], data[i]['k'], data[i]['l'], data[i]['twotheta'], data[i]['theta'], data[i]['chi'], data[i]['phi']];
                    
                    newData.push(tempData);
                }
                else {
                    tempIdealData = [data[i]['h'], data[i]['k'], data[i]['l'], data[i]['twotheta'], data[i]     ['theta'], data[i]['omega'], data[i]['chi'], data[i]['phi']];
                    
                    newIdealData.push(tempIdealData);
                }
            }
                
            store.loadData(newData);
            idealDataStore.loadData(newIdealData);
            
            isUBcalculated = data[0]['isUBcalculated'];
            myUBmatrix = data[0]['UBmatrix']

            UB11Field.setValue(myUBmatrix[0]);
            UB12Field.setValue(myUBmatrix[1]);
            UB13Field.setValue(myUBmatrix[2]);
            UB21Field.setValue(myUBmatrix[3]);
            UB22Field.setValue(myUBmatrix[4]);
            UB23Field.setValue(myUBmatrix[5]);
            UB31Field.setValue(myUBmatrix[6]);
            UB32Field.setValue(myUBmatrix[7]);
            UB33Field.setValue(myUBmatrix[8]);
            
            console.log(isUBcalculated);
        }
    };


    // ********* END - Handling loading and saving data  *********  
    
    // ************** Setting up the ComboBox ************** 
    var myComboStore = new Ext.data.ArrayStore({
        data: [[1, 'Bisecting'], [2, 'Scattering Plane'], [3, 'Phi Fixed']],
        fields: ['id', 'mode'],
        idIndex: 0
    });
    
    var myCombo = new Ext.form.ComboBox ({
        fieldLabel  : 'Select a Mode',
        store       : myComboStore,
        
        displayField: 'mode',
        typeAhead   : true,
        mode        : 'local',
        
        triggerAction:  'all', //Lets you see all drop down options when arrow is clicked
        selectOnFocus:  true,
        value        : 'Bisecting',
        
        listeners: {
            select: {
                fn: comboFunction
            }
        }
    });
    
    function comboFunction (combo, value) {
        //The comboBox gave a nasty object for value, hence the value['data']['mode']
        if (value['data']['mode'] == 'Bisecting'){
            //If switching to 'Bisecting' mode, removes special input boxes from other modes
            
            southPanel.removeAll(false); //sets auto-Destroy to false
            southPanel.setHeight(0);
            southPanel.add(ScatteringFieldset);

            southPanel.setTitle('No Mode-specific Inputs for Bisecting Mode');
            southPanel.doLayout(); //for already rendered panels, refreshes the layout
            
            innerRightTopPanel.doLayout();
        }
        else if (value['data']['mode'] == 'Scattering Plane'){
            //If switching to 'Scattering Plane' mode, removes other special input boxes from modes
            //and adds the scattering plane vectors input boxes
            
            southPanel.removeAll(false);
            southPanel.setHeight(91);
            southPanel.add(ScatteringFieldset);

            southPanel.setTitle('Scattering Plane Vectors');
            southPanel.doLayout();
            
            innerRightTopPanel.doLayout();
        }
        else if (value['data']['mode'] == 'Phi Fixed'){
            //If switching to 'Phi Fixed' mode, removes other special input boxes from modes
            //and adds the phi fixed value input box
            
            southPanel.removeAll(false);
            southPanel.setHeight(70);
            southPanel.add(PhiFixedFieldset);

            southPanel.setTitle('Fixed Phi Value');
            southPanel.doLayout();
            
            innerRightTopPanel.doLayout();
        }
        else{
            //Does nothing...
            console.log('else');
            //Ext.Msg.alert('Error: Could not save');
        }
    };

    
    //Setting up and rendering Panels 
    var southPanel = new Ext.Panel ({
        title   : 'No Mode-specific Inputs for Bisecting Mode',
        region  : 'south',
        margins : '0 5 0 0',
        height  : 0,
        id      : 'south-container'
    });
    
    var northPanel = new Ext.Panel ({
        region      : 'north',
        height      : 100,
        items       : [uploadPanel]
    });
    
    var innerLeftTopPanel = new Ext.Panel({
        layout: 'border',
        width: 440,
        height: 290, 
        items: [{
            region: 'center',
            items: [observationGrid]
        }, 
            northPanel,
        ]
    });

    var innerRightTopPanel = new Ext.Panel({
        layout: 'border',
        width: 350,
        height: 290,
        border: true,
        items: [{
            title   : 'Lattice Parameters',
            region  : 'center',
            id      : 'center-component',
            layout  : 'fit',
            margins : '0 5 0 0', //small margins to the east of box
            items   : [topFieldset]
        }, {
            title   : 'Choose the Mode',
            region  : 'north',
            height  : 50,
            margins : '0 5 0 0',
            items   : [myCombo]
        }, 
        southPanel
        ]
    });  

    var TopPanel = new Ext.Panel({
        layout: 'table',
        title: 'Known Data',
        width: 790,
        layoutConfig: {
            columns: 2
        },
        items: [innerLeftTopPanel, innerRightTopPanel]
    });

    var BottomPanel = new Ext.Panel({
        layout: 'table',
        //title: 'Desired Data',
        width: 790,
        layoutConfig: {
            columns: 2
        },
        items: [UBFieldset, grid2]
    });

    TopPanel.render('data-grid');
    BottomPanel.render('result-grid');
    
});

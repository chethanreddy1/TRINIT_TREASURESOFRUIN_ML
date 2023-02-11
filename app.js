function OnStart()
{       

	lay = app.CreateLayout( "linear", "VCenter,FillXY" )
	

	var msg = "GET / HTTP/1.1\r\n";
	
	n = app.CreateTextEdit( 'enter ratio of nitrogen in soil', 0.9, 0.07 ,'AutoSelect')
    n.SetBackColor( "#111111" )
	lay.AddChild( n )
	
	p = app.CreateTextEdit('enter ratio of phosporous in soil', 0.9, 0.07,'AutoSelect' )
    p.SetBackColor( "#111111" )
	lay.AddChild( p )

	k = app.CreateTextEdit( 'enter ratio of potassium in soil', 0.9, 0.07,'AutoSelect' )
    k.SetBackColor( "#111111" )
	lay.AddChild( k )

	c = app.CreateTextEdit( 'enter ph value', 0.9, 0.07, 'AutoSelect' )
    c.SetBackColor( "#111111" )
	lay.AddChild( c )
	
 	txt = app.CreateTextEdit( "", 0.9, 0.5, "ReadOnly,NoKeyboard" )
	txt.SetTextSize( 22 )
	txt.SetMargins( 0, 0.02, 0, 0 )
	txt.SetBackColor( "#111111" )
	lay.AddChild( txt )
	//Create Send button.
	btnSend = app.CreateButton( "Send", 0.4, -1 )
	btnSend.SetOnTouch( btnSend_OnTouch1 )
	lay.AddChild( btnSend )   
	


	app.AddLayout( lay )


	net = app.CreateNetClient( "TCP,Raw" )  
	net.SetOnConnect( net_OnConnect )
	net.Connect( "192.168.204.68", 5050 )
	    net.SetOnReceive( OnReceive );
    net.AutoReceive( "192.168.204.68", 5050, "UTF-8" );
		loc = app.CreateLocator( "GPS,Network" )
	loc.SetOnChange( loc_OnChange ) 
	loc.SetRate( 10 )
	loc.Start()

}
function loc_OnChange( data )
{
    lat=data.latitude
    lon=data.longitude

}

function net_OnConnect( connected )
{
	if( connected ) app.ShowPopup( "Connected!" )
	else net.Connect( "192.168.204.68", 5050 )
}

function btnSend_OnTouch1()
{

	if( !net.IsConnected() ) 
	{
	    app.ShowPopup( "Please connect" )
	    net.Connect( "192.168.204.68", 5050 )
	    
	}
    
	
	nv=n.GetText()
	pv=p.GetText()
	kv=k.GetText()
	cv=c.GetText()
	net.SendText( '/get/'+nv+'/'+pv+'/'+kv+'/'+lat+'/'+lon+'/'+cv, "UTF-8" )  


}

function OnReceive(s)
{

    txt.SetText( s )
    

}

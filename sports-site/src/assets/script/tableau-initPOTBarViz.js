function initPOTBarViz() {

    var containerDiv = document.getElementsByTagName('app-performance-over-time-bar').item(0).getElementsByTagName('div').item(0),
  
    url = "https://public.tableau.com/views/Trackv2/PerformanceOverTimeBar?:language=en&:display_count=y&:origin=viz_share_link",
  
    options = {
  
    height: 800,
  
    width: 1000,
  
    hideTabs: true,
  
    onFirstInteractive: function () {
  
    console.log("Run this code when the viz has finished loading.");
  
    }
  
    };
  
   
  
    if(viz != null) {
  
    viz.dispose();
  
    }
  
   
  
    var viz = new tableau.Viz(containerDiv, url, options);
  
    // Create a viz object and embed it in the container div.
  
   
  
  }
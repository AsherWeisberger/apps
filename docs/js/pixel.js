/* X Pixel companion. Base code lives in <head>. No-op if PIXEL_ID is empty or twq is already configured. Do not invent event IDs. */
(function () {
  var PIXEL_ID = "relo7";
  if (!PIXEL_ID) return;
  if (typeof window.twq === "function") return;
  !function(e,t,n,s,u,a){e.twq||(s=e.twq=function(){s.exe?s.exe.apply(s,arguments):s.queue.push(arguments);
  },s.version='1.1',s.queue=[],u=t.createElement(n),u.async=!0,u.src='https://static.ads-twitter.com/uwt.js',
  a=t.getElementsByTagName(n)[0],a.parentNode.insertBefore(u,a))}(window,document,'script');
  twq('config', PIXEL_ID);
})();

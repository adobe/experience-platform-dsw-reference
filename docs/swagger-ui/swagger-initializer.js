window.onload = function() {
  //<editor-fold desc="Changeable Configuration Block">

  // the following lines will be replaced by docker/configurator, when it runs in a docker-container
  window.ui = SwaggerUIBundle({
     url: "https://raw.githubusercontent.com/AdobeAtAdobe/kirby_docs/master/acpdr/swagger-specs/sensei-ml-api.yaml",
    dom_id: '#swagger-ui',
    deepLinking: true,
    presets: [
      SwaggerUIBundle.presets.apis
    ],
    plugins: [
      SwaggerUIBundle.plugins.DownloadUrl
    ]
  });

  //</editor-fold>
};

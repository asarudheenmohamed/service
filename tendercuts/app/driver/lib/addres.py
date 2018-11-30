<style><!--
#store-picker {
    padding: 15px;
}

#store-picker #google-maps {
    height: 300px
}

#store-picker p {
    font-style: normal;
}
#store-picker h3 {
    color: #bf202f;
}
#store-picker .card {
    border-radius: 3px;
    padding: 3px;
    margin: 31px 2% 7% 2%;
    border: 0px;
    cursor: pointer;
}
#store-picker p.google-location {
    text-align: center;
    margin: 20px
}

#store-picker p.google-location a {
    padding: 5px;
}
--></style>
<p>
<script type="text/javascript">// <![CDATA[
function init_map(){
        var myOptions = {
            zoom:10,
            center:new google.maps.LatLng(12.976271,80.22223800000006),
            mapTypeId: google.maps.MapTypeId.ROADMAP};

        var locations = [
        {
            "id": "velachery",
            "address": '<strong>velachery</strong><br>Plot No:1, No:44/1, Sarathy Nagar, Velachery Chennai, Tamil Nadu<br>600042 chennai<br>',
            "location": new google.maps.LatLng(12.976271,80.22223800000006)
        },
        {
            "id": "thoraipakkam",
            "address": '<strong>Thoraipakkam</strong><br>5/350, Rajiv Gandhi Main Road,OMR, Thoraipakkam Chennai, Tamil Nadu <br>600097 chennai<br>',
            "location": new google.maps.LatLng(12.928171,80.235877)
        },
        {
            "id": "valasaravakkam",
            "address": '<strong>Valasaravakkam</strong><br>No:47, Arcot Road, Valasaravakkam Chennai Tamil Nadu <br>600087 chennai<br>',
            "location": new google.maps.LatLng(13.037924,80.163725)
        },
        {
            "id": "mogappair",
            "address": '<strong>Mogappair</strong><br>Shanghai Dhaba Building, 3PC 17, Main Road, Mogappair West  Chennai, Tamil Nadu<br>600037 chennai<br>',
            "location": new google.maps.LatLng(13.083098,80.171446)
        },
        {
            "id": "medavakkam",
            "address": '<strong>Medavakkam</strong><br>No:4/787, velachery main road, near jeyachander Textiles  <br>600037 chennai<br>',
            "location": new google.maps.LatLng(12.9190916,80.1963286)
        },
        {
            "id": "chrompet",
            "address": '<strong>Chrompet</strong><br>No: 9, C.L.C Works Road,<br>600044 chennai<br>',
            "location": new google.maps.LatLng(12.953368, 80.139127)
        },
        {
            "id": "adayar",
            "address": '<strong>Adayar</strong><br>No,48 TNHB Comblex,<br>600020 chennai<br>',
            "location": new google.maps.LatLng(13.000252, 80.256485)
        },
        {
            "id": "navalur",
            "address": '<strong>Navalur</strong><br>No.4/43 Rajiv Gandhi Salai,<br>600130 chennai<br>',
            "location": new google.maps.LatLng(12.849116, 80.226760)
        },
       {
            "id": "madanandapuram",
            "address": '<strong>Madanandapuram </strong><br>No-54, Guruswamy nagar, mugalivakkam main road,<br>600116 chennai<br>',
            "location": new google.maps.LatLng(13.021843, 80.154353)
        },
       {
          "id": "kattupakkam",
          "address": '<strong>Kattupakkam</strong><br>No.2/10, Mount Poonamallee Main Road,<br>Chennai - 600056<br>',
          "location": new google.maps.LatLng(13.040566, 80.129013 )
       },

        ];

        function onClick(marker, infowindow, map, location) {
            return function() {
                infowindow.setContent(location.address);
                infowindow.open(map, marker);
                map.setCenter(marker.getPosition())
            }
        }

        var map = new google.maps.Map(document.getElementById('google-maps'), myOptions);
        var infowindow = new google.maps.InfoWindow();
        for (var i = locations.length - 1; i >= 0; i--) {
            var marker = new google.maps.Marker({map: map, position: locations[i].location});
            google.maps.event.addListener(marker, 'click', onClick(marker, infowindow, map, locations[i]));

            document.getElementById(locations[i].id).addEventListener(
                'click',
                onClick(marker, infowindow, map, locations[i])
            );
        }
    }

    google.maps.event.addDomListener(window, 'load', init_map);
// ]]></script>
</p>
<div id="store-picker">
<div id="google-maps" class="row">&nbsp;</div>
<div class="row">
<div id="velachery" class="col-md-3">
<div class="card">
<div class="card-block">
<h3 class="card-title">Velachery</h3>
<p class="card-text">Plot No:1, No:44/1, Sarathy Nagar</p>
<p class="card-text">Sarathy Nagar</p>
<p class="card-text">Velachery Chennai-600042</p>
<p class="card-text">Ph:<a href="tel:9543754375">9543754375</a></p>
</div>
</div>
</div>
<div id="thoraipakkam" class="col-md-3">
<div class="card">
<div class="card-block">
<h3 class="card-title">Thoraipakkam</h3>
<p class="card-text">Plot: 5/350, Rajiv Gandhi Main Road,OMR</p>
<p class="card-text">Thoraipakkam Chennai -600097</p>
<p class="card-text">Ph:<a href="tel:9543754375">9543754375</a></p>
</div>
</div>
</div>
<div id="valasaravakkam" class="col-md-3">
<div class="card">
<div class="card-block">
<h3 class="card-title">Valasaravakkam</h3>
<p class="card-text">No:47, Arcot Road</p>
<p class="card-text">Valasaravakkam Chennai-600087</p>
<p class="card-text">Chennai-600087</p>
<p class="card-text">Ph:<a href="tel:9543754375">9543754375</a></p>
</div>
</div>
</div>
<div id="mogappair" class="col-md-3">
<div class="card">
<div class="card-block">
<h3 class="card-title">Mogappair</h3>
<p class="card-text">Shanghai Dhaba Building</p>
<p class="card-text">3PC 17, Main Road</p>
<p class="card-text">Mogappair Chennai-600037</p>
<p class="card-text">Ph:<a href="tel:9543754375">9543754375</a></p>
</div>
</div>
</div>
<div id="medavakkam" class="col-md-3">
<div class="card">
<div class="card-block">
<h3 class="card-title">Medavakkam</h3>
<p class="card-text">Velachery main road,</p>
<p class="card-text">Near jeyachander Textiles</p>
<p class="card-text">Medavakkam Chennai-600100</p>
<p class="card-text">Ph:<a href="tel:9543754375">9543754375</a></p>
</div>
</div>
</div>
<div id="chrompet" class="col-md-3">
<div class="card">
<div class="card-block">
<h3 class="card-title">Chrompet</h3>
<p class="card-text">No: 9, C.L.C Works Road,</p>
<p class="card-text">Chrompet Chennai-600044</p>
<p class="card-text">Ph:<a href="tel:9543754375">9543754375</a></p>
<p class="card-text">&nbsp;</p>
</div>
</div>
</div>
<div id="adayar" class="col-md-3">
<div class="card">
<div class="card-block">
<h3 class="card-title">Adayar</h3>
<p class="card-text">No,48 TNHB Comblex,</p>
<p class="card-text">LB Road (Near BSNL Ex),</p>
<p class="card-text">Adyar Chennai-600020</p>
<p class="card-text">Ph:<a href="tel:9543754375">9543754375</a></p>
</div>
</div>
</div>
<div id="navalur" class="col-md-3">
<div class="card">
<div class="card-block">
<h3 class="card-title">Navalur</h3>
<p class="card-text">No.4/43 Rajiv Gandhi Salai,</p>
<p class="card-text">Navalur Chennai-600130</p>
<p class="card-text">Ph:<a href="tel:9543754375">9543754375</a></p>
<p class="card-text">&nbsp;</p>
</div>
</div>
</div>
<div id="madanandapuram" class="col-md-3">
<div class="card">
<div class="card-block">
<h3 class="card-title">Madanandapuram</h3>
<p class="card-text">No-54, Guruswamy nagar,</p>
<p class="card-text">Mugalivakkam main road,</p>
<p class="card-text">Next to Sri Murugan stores,</p>
<p class="card-text">Madanandapuram, Chennai -600116.</p>
<p class="card-text">Ph:<a href="tel:9543754375">9543754375</a></p>
<p class="card-text">&nbsp;</p>
</div>
</div>
</div>
<div id="kattupakkam" class="col-md-3">
<div class="card">
<div class="card-block">
<h3 class="card-title">Kattupakkam</h3>
<p class="card-text">No.2/10, Mount Poonamallee Main Road, Near Kattupakkam bus stop and before Kalashetra School,</p>
<p class="card-text">Kattupakkam, Chennai &ndash; 600056</p>
<p class="card-text">Ph:<a href="tel:9543754375">9543754375</a></p>
<p class="card-text">&nbsp;</p>
</div>
</div>
</div>
</div>
</div>
import React, { useEffect } from "react";

import L from "leaflet";
import "leaflet/dist/leaflet.css";

//@ts-ignore
import axios from "../../utils/axios";

import "../../MarkerCluster.css";
import "../../MarkerCluster.Default.css";
import "leaflet.markercluster";
import { useMapStore } from "../../store/MapStateStore";
import {
  fetchPaddockGeometry,
  fetchSectionsData,
  satelliteMap,
  sentinelMap,
} from "../../utils/map";
import { useQuery } from "react-query";
import {
  InitializeMap,
  addSections,
  drawPaddock,
  drawPiezometers,
} from "../../utils/mapInitFunc";
import { FadeLoader } from "react-spinners";
import { incidentIcon } from "../../utils/icons";
import moment from "moment";
import SkeletonIncidentLocationShowcaseMap from "../Skeletons/Incidents/SkeletonIncidentLocationShowcaseMap";

function IncidentLocationShowcaseMap({
  information,
}: {
  information: {
    paddock: string;
    latitude: string | number;
    longitude: string | number;
  };
}) {
  const current_zoom = 14;
  const basemap = useMapStore((state) => state.basemap);
  const changeBasemap = useMapStore((state) => state.changeBasemap);

  let baselayer: L.Control.Layers;

  let sections: L.GeoJSON<any>;

  let myMap: L.Map | L.LayerGroup<any> | undefined;
  // @ts-ignore: Unreachable code error
  let piezometers = [];

  const fetchSectionsData = async () => {
    const result = await axios.get("/get_geojson_sections-sections_bp");

    return result.data[0].features;
  };

  const { isLoading: sectionsAreLoading, data: sectionsData } = useQuery(
    "sections",
    fetchSectionsData,
    {
      refetchOnWindowFocus: false,
    }
  );

  const { isLoading: paddocksAreLoading, data: paddockData } = useQuery({
    queryKey: [`paddock-${information.paddock ? information.paddock : "None"}`],
    queryFn: () => fetchPaddockGeometry({ paddock: information.paddock }),
    refetchOnWindowFocus: false,
  });

  const markers = L.markerClusterGroup();

  async function DrawIncidentsShowcaseMap({ current_zoom, mapDOM }: any) {
    const satellite = await satelliteMap();
    const sentinelHub = await sentinelMap(
      moment(Date.now()).format("MM-DD-YYYY")
    );

    const myMap = L.map(mapDOM, {
      center: L.latLng(
        Number(information.latitude),
        Number(information.longitude)
      ),
      zoom: current_zoom,
      //@ts-ignore
      layers: basemap === "satellite" ? satellite : sentinelHub,
      fadeAnimation: true,
      zoomAnimation: true,
    });

    //base maps
    const baseMaps = {
      Satellite: satellite,
      "Moisture Index": sentinelHub,
    };

    // @ts-ignore
    const baselayer = L.control.layers(baseMaps).addTo(myMap);

    // @ts-ignore
    myMap.on("baselayerchange", function (event) {
      switch (event.layer) {
        case sentinelHub:
          changeBasemap("sentinel");
          break;
        case satellite:
          changeBasemap("satellite");
          break;
      }
    });

    return myMap;
  }

  async function drawIncident({ piezometers, map, markers }: any) {
    // adding circles to the map
    // @ts-ignore

    let icon = incidentIcon;

    const circle = L.marker(
      [Number(information.latitude), Number(information.longitude)],
      {
        icon: icon,
      }
    );
    circle.bindPopup(`
          <div class="flex flex-col gap-y-4">
            
            <div class="flex items-center gap-x-4">
              <span class="font-semibold text-xs">Paddock section: </span>
              <span>${information.paddock}</span>
            </div>
  
            <div class="flex flex-col gap-y-2" >
              <span class="font-semibold text-xs" >Location coordinates: </span>
              <span>${information.latitude}° / ${information.longitude}°</span>
            </div>
          </div>
        `);

    markers.addLayer(circle);
    piezometers.push(circle);

    map?.addLayer(markers);
  }

  // @ts-ignore
  const init = async () => {
    //Re - initialize the map
    myMap = await DrawIncidentsShowcaseMap({
      current_zoom,
      mapDOM: "mapIncidentShowcase",
    });

    sections = await addSections({ sectionsData, map: myMap });

    await drawPaddock({
      map: myMap,
      paddockData,
    });

    //Draw piezometers using the filtered list
    //@ts-ignore
    await drawIncident({ piezometers, map: myMap, markers });
  };

  useEffect(() => {
    if (!sectionsAreLoading || !paddocksAreLoading) init();
  }, []);

  useEffect(() => {
    if (!sectionsAreLoading || !paddocksAreLoading) init();
  }, [sectionsAreLoading, paddocksAreLoading]);

  if (sectionsAreLoading || paddocksAreLoading)
    return <SkeletonIncidentLocationShowcaseMap />;

  return (
    <div className="  w-full   h-[50vh]  rounded-[14px] overflow-hidden shadow-md relative z-[10]">
      <div id="mapIncidentShowcase"></div>
    </div>
  );
}

export default IncidentLocationShowcaseMap;

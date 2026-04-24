import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Parkingavailability: React.FC = () => {
  return (
    <div id="page-parkingavailability-1">
    <div id="i78u7" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="ijz03" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="ixz7h" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="i06p5" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="i8aeh" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/parkingplace">{"ParkingPlace"}</a>
          <a id="ilvn9" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/parkingavailability">{"ParkingAvailability"}</a>
        </div>
        <p id="idpfh" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="igte8" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="i5xjw" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"ParkingAvailability"}</h1>
        <p id="iyt2h" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage ParkingAvailability data"}</p>
        <TableBlock id="table-parkingavailability-1" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="ParkingAvailability List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "AvailabilityId", "column_type": "field", "field": "availabilityId", "type": "str", "required": true}, {"label": "CheckedAt", "column_type": "field", "field": "checkedAt", "type": "date", "required": true}, {"label": "AnyPlaceFree", "column_type": "field", "field": "anyPlaceFree", "type": "bool", "required": true}, {"label": "BothPlacesFree", "column_type": "field", "field": "bothPlacesFree", "type": "bool", "required": true}, {"label": "HasPlaces", "column_type": "lookup", "path": "hasPlaces", "entity": "ParkingPlace", "field": "placeId", "type": "list", "required": true}], "formColumns": [{"column_type": "field", "field": "availabilityId", "label": "availabilityId", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "checkedAt", "label": "checkedAt", "type": "date", "required": true, "defaultValue": null}, {"column_type": "field", "field": "anyPlaceFree", "label": "anyPlaceFree", "type": "bool", "required": true, "defaultValue": null}, {"column_type": "field", "field": "bothPlacesFree", "label": "bothPlacesFree", "type": "bool", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "hasPlaces", "field": "hasPlaces", "lookup_field": "placeId", "entity": "ParkingPlace", "type": "list", "required": true}]}} dataBinding={{"entity": "ParkingAvailability", "endpoint": "/parkingavailability/"}} />
        <div id="ibho2" style={{"marginTop": "20px", "display": "flex", "--chart-color-palette": "default", "flexWrap": "wrap", "gap": "10px"}}>
          <MethodButton id="iscfn" className="action-button-component" style={{"padding": "6px 14px", "fontSize": "13px", "fontWeight": "600", "textDecoration": "none", "letterSpacing": "0.01em", "display": "flex", "cursor": "pointer", "transition": "background 0.2s", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "borderRadius": "4px", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "--chart-color-palette": "default", "alignItems": "center"}} endpoint="/parkingavailability/{parkingavailability_id}/methods/refreshAvailabilityStatus/" label="refreshAvailabilityStatus" isInstanceMethod={true} instanceSourceTableId="table-parkingavailability-1" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Parkingavailability;

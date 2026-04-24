import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Parkingplace: React.FC = () => {
  return (
    <div id="page-parkingplace-0">
    <div id="ijbw3" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="isqnf" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="i2lao" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="itj6z" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="iodlw" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/parkingplace">{"ParkingPlace"}</a>
          <a id="i6bvu" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/parkingavailability">{"ParkingAvailability"}</a>
        </div>
        <p id="i0qtj" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="ie9l8" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="iffgi" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"ParkingPlace"}</h1>
        <p id="i2oab" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage ParkingPlace data"}</p>
        <TableBlock id="table-parkingplace-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="ParkingPlace List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "PlaceId", "column_type": "field", "field": "placeId", "type": "str", "required": true}, {"label": "IsFree", "column_type": "field", "field": "isFree", "type": "bool", "required": true}, {"label": "LastUpdated", "column_type": "field", "field": "lastUpdated", "type": "date", "required": true}, {"label": "LocationDescription", "column_type": "field", "field": "locationDescription", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "placeId", "label": "placeId", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "isFree", "label": "isFree", "type": "bool", "required": true, "defaultValue": "true"}, {"column_type": "field", "field": "lastUpdated", "label": "lastUpdated", "type": "date", "required": true, "defaultValue": null}, {"column_type": "field", "field": "locationDescription", "label": "locationDescription", "type": "str", "required": false, "defaultValue": null}, {"column_type": "lookup", "path": "parkingavailability", "field": "parkingavailability", "lookup_field": "availabilityId", "entity": "ParkingAvailability", "type": "str", "required": true}]}} dataBinding={{"entity": "ParkingPlace", "endpoint": "/parkingplace/"}} />
        <div id="i9tbg" style={{"marginTop": "20px", "display": "flex", "--chart-color-palette": "default", "flexWrap": "wrap", "gap": "10px"}}>
          <MethodButton id="i9ra6" className="action-button-component" style={{"padding": "6px 14px", "fontSize": "13px", "fontWeight": "600", "textDecoration": "none", "letterSpacing": "0.01em", "display": "flex", "cursor": "pointer", "transition": "background 0.2s", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "borderRadius": "4px", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "--chart-color-palette": "default", "alignItems": "center"}} endpoint="/parkingplace/{parkingplace_id}/methods/updateAvailability/" label="updateAvailability" parameters={[{"name": "freeStatus", "type": "bool", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-parkingplace-0" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Parkingplace;

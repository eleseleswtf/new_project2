####################
# STRUCTURAL MODEL #
####################

from besser.BUML.metamodel.structural import (
    Class, Property, Method, Parameter,
    BinaryAssociation, Generalization, DomainModel,
    Enumeration, EnumerationLiteral, Multiplicity,
    StringType, IntegerType, FloatType, BooleanType,
    TimeType, DateType, DateTimeType, TimeDeltaType,
    AnyType, Constraint, AssociationClass, Metadata, MethodImplementationType
)

# Classes
ParkingPlace = Class(name="ParkingPlace")
Garage = Class(name="Garage")

# ParkingPlace class attributes and methods
ParkingPlace_placeId: Property = Property(name="placeId", type=StringType, visibility="private")
ParkingPlace_isFree: Property = Property(name="isFree", type=BooleanType, visibility="private")
ParkingPlace_lastUpdated: Property = Property(name="lastUpdated", type=DateType, visibility="private")
ParkingPlace_locationDescription: Property = Property(name="locationDescription", type=StringType, visibility="private", is_optional=True)
ParkingPlace_m_updateAvailability: Method = Method(name="updateAvailability", parameters={Parameter(name='freeStatus', type=BooleanType)}, implementation_type=MethodImplementationType.NONE)
ParkingPlace.attributes={ParkingPlace_isFree, ParkingPlace_lastUpdated, ParkingPlace_locationDescription, ParkingPlace_placeId}
ParkingPlace.methods={ParkingPlace_m_updateAvailability}

# Garage class attributes and methods
Garage_availabilityId: Property = Property(name="availabilityId", type=StringType, visibility="private")
Garage_checkedAt: Property = Property(name="checkedAt", type=DateType, visibility="private")
Garage_anyPlaceFree: Property = Property(name="anyPlaceFree", type=BooleanType, visibility="private", is_derived=True)
Garage_bothPlacesFree: Property = Property(name="bothPlacesFree", type=BooleanType, visibility="private", is_derived=True)
Garage_m_refreshAvailabilityStatus: Method = Method(name="refreshAvailabilityStatus", parameters={}, implementation_type=MethodImplementationType.NONE)
Garage.attributes={Garage_anyPlaceFree, Garage_availabilityId, Garage_bothPlacesFree, Garage_checkedAt}
Garage.methods={Garage_m_refreshAvailabilityStatus}

# Relationships
hasPlaces: BinaryAssociation = BinaryAssociation(
    name="hasPlaces",
    ends={
        Property(name="parkingplace", type=ParkingPlace, multiplicity=Multiplicity(2, 2)),
        Property(name="hasPlaces", type=Garage, multiplicity=Multiplicity(1, 1))
    }
)

# Domain Model
domain_model = DomainModel(
    name="Class_Diagram",
    types={ParkingPlace, Garage},
    associations={hasPlaces},
    generalizations={},
    metadata=None
)


###############
#  GUI MODEL  #
###############

from besser.BUML.metamodel.gui import (
    GUIModel, Module, Screen,
    ViewComponent, ViewContainer,
    Button, ButtonType, ButtonActionType,
    Text, Image, Link, InputField, InputFieldType,
    Form, Menu, MenuItem, DataList,
    DataSource, DataSourceElement, EmbeddedContent,
    Styling, Size, Position, Color, Layout, LayoutType,
    UnitSize, PositionType, Alignment
)
from besser.BUML.metamodel.gui.dashboard import (
    LineChart, BarChart, PieChart, RadarChart, RadialBarChart, Table, AgentComponent,
    Column, FieldColumn, LookupColumn, ExpressionColumn, MetricCard, Series
)
from besser.BUML.metamodel.gui.events_actions import (
    Event, EventType, Transition, Create, Read, Update, Delete, Parameter
)
from besser.BUML.metamodel.gui.binding import DataBinding

# Module: GUI_Module

# Screen: wrapper
wrapper = Screen(name="wrapper", description="ParkingPlace", view_elements=set(), is_main_page=True, route_path="/parkingplace", screen_size="Medium")
wrapper.component_id = "page-parkingplace-0"
i2lao = Text(
    name="i2lao",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="i2lao",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "i2lao"}
)
iodlw = Link(
    name="iodlw",
    description="Link element",
    label="ParkingPlace",
    url="/parkingplace",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iodlw",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/parkingplace", "id": "iodlw"}
)
i6bvu = Link(
    name="i6bvu",
    description="Link element",
    label="ParkingAvailability",
    url="/parkingavailability",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i6bvu",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/parkingavailability", "id": "i6bvu"}
)
itj6z = ViewContainer(
    name="itj6z",
    description=" component",
    view_elements={iodlw, i6bvu},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="itj6z",
    display_order=1,
    custom_attributes={"id": "itj6z"}
)
itj6z_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
itj6z.layout = itj6z_layout
i0qtj = Text(
    name="i0qtj",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="i0qtj",
    display_order=2,
    custom_attributes={"id": "i0qtj"}
)
isqnf = ViewContainer(
    name="isqnf",
    description="nav container",
    view_elements={i2lao, itj6z, i0qtj},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="isqnf",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "isqnf"}
)
isqnf_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
isqnf.layout = isqnf_layout
iffgi = Text(
    name="iffgi",
    content="ParkingPlace",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="iffgi",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "iffgi"}
)
i2oab = Text(
    name="i2oab",
    content="Manage ParkingPlace data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="i2oab",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "i2oab"}
)
table_parkingplace_0_col_0 = FieldColumn(label="PlaceId", field=ParkingPlace_placeId)
table_parkingplace_0_col_1 = FieldColumn(label="IsFree", field=ParkingPlace_isFree)
table_parkingplace_0_col_2 = FieldColumn(label="LastUpdated", field=ParkingPlace_lastUpdated)
table_parkingplace_0_col_3 = FieldColumn(label="LocationDescription", field=ParkingPlace_locationDescription)
table_parkingplace_0 = Table(
    name="table_parkingplace_0",
    title="ParkingPlace List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_parkingplace_0_col_0, table_parkingplace_0_col_1, table_parkingplace_0_col_2, table_parkingplace_0_col_3],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-parkingplace-0",
    display_order=2,
    css_classes=["has-data-binding"],
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "ParkingPlace List", "data-source": "class_58seo5nao_mocu1r36_gwj", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'placeId', 'label': 'PlaceId', 'columnType': 'field', '_expanded': False}, {'field': 'isFree', 'label': 'IsFree', 'columnType': 'field', '_expanded': False}, {'field': 'lastUpdated', 'label': 'LastUpdated', 'columnType': 'field', '_expanded': False}, {'field': 'locationDescription', 'label': 'LocationDescription', 'columnType': 'field', '_expanded': False}, {'field': 'ParkingAvailability', 'label': 'ParkingAvailability', 'columnType': 'lookup', 'lookupEntity': 'class_lkd9lx6es_mocu1r37_168', 'lookupField': 'availabilityId', '_expanded': False}], "id": "table-parkingplace-0", "filter": ""}
)
domain_model_ref = globals().get('domain_model') or next((v for k, v in globals().items() if k.startswith('domain_model') and hasattr(v, 'get_class_by_name')), None)
table_parkingplace_0_binding_domain = None
if domain_model_ref is not None:
    table_parkingplace_0_binding_domain = domain_model_ref.get_class_by_name("ParkingPlace")
if table_parkingplace_0_binding_domain:
    table_parkingplace_0_binding = DataBinding(domain_concept=table_parkingplace_0_binding_domain, name="ParkingPlaceDataBinding")
else:
    # Domain class 'ParkingPlace' not resolved; data binding skipped.
    table_parkingplace_0_binding = None
if table_parkingplace_0_binding:
    table_parkingplace_0.data_binding = table_parkingplace_0_binding
i9ra6 = Button(
    name="i9ra6",
    description="Button component",
    label="updateAvailability",
    buttonType=ButtonType.CustomizableButton,
    actionType=ButtonActionType.RunMethod,
    method_btn=ParkingPlace_m_updateAvailability,
    instance_source="table-parkingplace-0",
    is_instance_method=True,
    styling=Styling(size=Size(padding="6px 14px", font_size="13px", font_weight="600", text_decoration="none", letter_spacing="0.01em"), position=Position(display="inline-flex", cursor="pointer", transition="background 0.2s"), color=Color(background_color="linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", text_color="#fff", color_palette="default", border_radius="4px", border="none", box_shadow="0 1px 4px rgba(37,99,235,0.10)"), layout=Layout(layout_type=LayoutType.FLEX, align_items="center")),
    component_id="i9ra6",
    tag_name="button",
    display_order=0,
    css_classes=["action-button-component"],
    custom_attributes={"type": "button", "data-button-label": "updateAvailability", "data-action-type": "run-method", "data-method": "method_rvhw9wsa2_mocu1r36_niy", "data-instance-source": "table-parkingplace-0", "id": "i9ra6", "method-class": "ParkingPlace", "endpoint": "/parkingplace/{parkingplace_id}/methods/updateAvailability/", "is-instance-method": "true", "input-parameters": {'freeStatus': {'type': 'bool', 'required': True}}, "instance-source": "table-parkingplace-0"}
)
i9tbg = ViewContainer(
    name="i9tbg",
    description=" component",
    view_elements={i9ra6},
    styling=Styling(size=Size(margin_top="20px"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_wrap="wrap", gap="10px")),
    component_id="i9tbg",
    display_order=3,
    custom_attributes={"id": "i9tbg"}
)
i9tbg_layout = Layout(layout_type=LayoutType.FLEX, flex_wrap="wrap", gap="10px")
i9tbg.layout = i9tbg_layout
ie9l8 = ViewContainer(
    name="ie9l8",
    description="main container",
    view_elements={iffgi, i2oab, table_parkingplace_0, i9tbg},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="ie9l8",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "ie9l8"}
)
ie9l8_layout = Layout(flex="1")
ie9l8.layout = ie9l8_layout
ijbw3 = ViewContainer(
    name="ijbw3",
    description=" component",
    view_elements={isqnf, ie9l8},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="ijbw3",
    display_order=0,
    custom_attributes={"id": "ijbw3"}
)
ijbw3_layout = Layout(layout_type=LayoutType.FLEX)
ijbw3.layout = ijbw3_layout
wrapper.view_elements = {ijbw3}


# Screen: wrapper_2
wrapper_2 = Screen(name="wrapper_2", description="ParkingAvailability", view_elements=set(), route_path="/parkingavailability", screen_size="Medium")
wrapper_2.component_id = "page-parkingavailability-1"
ixz7h = Text(
    name="ixz7h",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="ixz7h",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "ixz7h"}
)
i8aeh = Link(
    name="i8aeh",
    description="Link element",
    label="ParkingPlace",
    url="/parkingplace",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i8aeh",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/parkingplace", "id": "i8aeh"}
)
ilvn9 = Link(
    name="ilvn9",
    description="Link element",
    label="ParkingAvailability",
    url="/parkingavailability",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ilvn9",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/parkingavailability", "id": "ilvn9"}
)
i06p5 = ViewContainer(
    name="i06p5",
    description=" component",
    view_elements={i8aeh, ilvn9},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="i06p5",
    display_order=1,
    custom_attributes={"id": "i06p5"}
)
i06p5_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
i06p5.layout = i06p5_layout
idpfh = Text(
    name="idpfh",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="idpfh",
    display_order=2,
    custom_attributes={"id": "idpfh"}
)
ijz03 = ViewContainer(
    name="ijz03",
    description="nav container",
    view_elements={ixz7h, i06p5, idpfh},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="ijz03",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "ijz03"}
)
ijz03_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
ijz03.layout = ijz03_layout
i5xjw = Text(
    name="i5xjw",
    content="ParkingAvailability",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="i5xjw",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "i5xjw"}
)
iyt2h = Text(
    name="iyt2h",
    content="Manage ParkingAvailability data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="iyt2h",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "iyt2h"}
)
table_parkingavailability_1_col_0 = FieldColumn(label="AvailabilityId", field=Garage_availabilityId)
table_parkingavailability_1_col_1 = FieldColumn(label="CheckedAt", field=Garage_checkedAt)
table_parkingavailability_1_col_2 = FieldColumn(label="AnyPlaceFree", field=Garage_anyPlaceFree)
table_parkingavailability_1_col_3 = FieldColumn(label="BothPlacesFree", field=Garage_bothPlacesFree)
table_parkingavailability_1 = Table(
    name="table_parkingavailability_1",
    title="ParkingAvailability List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_parkingavailability_1_col_0, table_parkingavailability_1_col_1, table_parkingavailability_1_col_2, table_parkingavailability_1_col_3],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-parkingavailability-1",
    display_order=2,
    css_classes=["has-data-binding"],
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "ParkingAvailability List", "data-source": "class_lkd9lx6es_mocu1r37_168", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'availabilityId', 'label': 'AvailabilityId', 'columnType': 'field', '_expanded': False}, {'field': 'checkedAt', 'label': 'CheckedAt', 'columnType': 'field', '_expanded': False}, {'field': 'anyPlaceFree', 'label': 'AnyPlaceFree', 'columnType': 'field', '_expanded': False}, {'field': 'bothPlacesFree', 'label': 'BothPlacesFree', 'columnType': 'field', '_expanded': False}, {'field': 'hasPlaces', 'label': 'HasPlaces', 'columnType': 'lookup', 'lookupEntity': 'class_58seo5nao_mocu1r36_gwj', 'lookupField': 'placeId', '_expanded': False}], "id": "table-parkingavailability-1", "filter": ""}
)
domain_model_ref = globals().get('domain_model') or next((v for k, v in globals().items() if k.startswith('domain_model') and hasattr(v, 'get_class_by_name')), None)
table_parkingavailability_1_binding_domain = None
if domain_model_ref is not None:
    table_parkingavailability_1_binding_domain = domain_model_ref.get_class_by_name("Garage")
if table_parkingavailability_1_binding_domain:
    table_parkingavailability_1_binding = DataBinding(domain_concept=table_parkingavailability_1_binding_domain, name="GarageDataBinding")
else:
    # Domain class 'Garage' not resolved; data binding skipped.
    table_parkingavailability_1_binding = None
if table_parkingavailability_1_binding:
    table_parkingavailability_1.data_binding = table_parkingavailability_1_binding
iscfn = Button(
    name="iscfn",
    description="Button component",
    label="refreshAvailabilityStatus",
    buttonType=ButtonType.CustomizableButton,
    actionType=ButtonActionType.RunMethod,
    method_btn=Garage_m_refreshAvailabilityStatus,
    instance_source="table-parkingavailability-1",
    is_instance_method=True,
    confirmation_message="Are you sure?",
    styling=Styling(size=Size(padding="6px 14px", font_size="13px", font_weight="600", text_decoration="none", letter_spacing="0.01em"), position=Position(display="inline-flex", cursor="pointer", transition="background 0.2s"), color=Color(background_color="linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", text_color="#fff", color_palette="default", border_radius="4px", border="none", box_shadow="0 1px 4px rgba(37,99,235,0.10)"), layout=Layout(layout_type=LayoutType.FLEX, align_items="center")),
    component_id="iscfn",
    tag_name="button",
    display_order=0,
    css_classes=["action-button-component"],
    custom_attributes={"type": "button", "data-button-label": "refreshAvailabilityStatus", "data-action-type": "run-method", "data-method": "method_3xm4bkznq_mocu1r37_fbn", "data-instance-source": "table-parkingavailability-1", "id": "iscfn", "data-confirmation": "false", "data-confirmation-message": "Are you sure?", "button-label": "refreshAvailabilityStatus", "method-name": "refreshAvailabilityStatus", "method-class": "Garage", "endpoint": "/garage/{garage_id}/methods/refreshAvailabilityStatus/", "is-instance-method": "true", "instance-source": "table-parkingavailability-1"}
)
ibho2 = ViewContainer(
    name="ibho2",
    description=" component",
    view_elements={iscfn},
    styling=Styling(size=Size(margin_top="20px"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_wrap="wrap", gap="10px")),
    component_id="ibho2",
    display_order=3,
    custom_attributes={"id": "ibho2"}
)
ibho2_layout = Layout(layout_type=LayoutType.FLEX, flex_wrap="wrap", gap="10px")
ibho2.layout = ibho2_layout
igte8 = ViewContainer(
    name="igte8",
    description="main container",
    view_elements={i5xjw, iyt2h, table_parkingavailability_1, ibho2},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="igte8",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "igte8"}
)
igte8_layout = Layout(flex="1")
igte8.layout = igte8_layout
i78u7 = ViewContainer(
    name="i78u7",
    description=" component",
    view_elements={ijz03, igte8},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="i78u7",
    display_order=0,
    custom_attributes={"id": "i78u7"}
)
i78u7_layout = Layout(layout_type=LayoutType.FLEX)
i78u7.layout = i78u7_layout
wrapper_2.view_elements = {i78u7}

gui_module = Module(
    name="GUI_Module",
    screens={wrapper, wrapper_2}
)

# GUI Model
gui_model = GUIModel(
    name="GUI",
    package="",
    versionCode="1.0",
    versionName="1.0",
    modules={gui_module},
    description="GUI"
)

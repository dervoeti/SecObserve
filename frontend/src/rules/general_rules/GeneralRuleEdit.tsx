import {
    BooleanInput,
    DeleteButton,
    Edit,
    ReferenceInput,
    SaveButton,
    SelectInput,
    SimpleForm,
    Toolbar,
    required,
} from "react-admin";

import { AutocompleteInputMedium, TextInputWide } from "../../commons/layout/themes";
import { OBSERVATION_SEVERITY_CHOICES, OBSERVATION_STATUS_CHOICES } from "../../core/types";

const CustomToolbar = () => {
    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton />
            <DeleteButton mutationMode="pessimistic" />
        </Toolbar>
    );
};

const transform = (data: any) => {
    if (data.scanner_prefix == null) {
        data.scanner_prefix = "";
    }
    if (data.title == null) {
        data.title = "";
    }
    if (data.description_observation == null) {
        data.description_observation = "";
    }
    if (data.origin_component_name_version == null) {
        data.origin_component_name_version = "";
    }
    if (data.origin_docker_image_name_tag == null) {
        data.origin_docker_image_name_tag = "";
    }
    if (data.origin_endpoint_url == null) {
        data.origin_endpoint_url = "";
    }
    if (data.origin_service_name == null) {
        data.origin_service_name = "";
    }
    if (data.origin_source_file == null) {
        data.origin_source_file = "";
    }
    if (data.origin_cloud_qualified_resource == null) {
        data.origin_cloud_qualified_resource = "";
    }
    if (data.new_severity == null) {
        data.new_severity = "";
    }
    if (data.new_status == null) {
        data.new_status = "";
    }
    return data;
};

const GeneralRuleEdit = () => {
    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
                <TextInputWide autoFocus source="name" validate={requiredValidate} />
                <TextInputWide multiline source="description" />
                <ReferenceInput source="parser" reference="parsers" sort={{ field: "name", order: "ASC" }}>
                    <SelectInput optionText="name" />
                </ReferenceInput>
                <TextInputWide source="scanner_prefix" />
                <TextInputWide
                    source="title"
                    label="Observation title"
                    helperText="Regular expression to match the observation's title"
                />
                <TextInputWide
                    source="description_observation"
                    label="Observation description"
                    helperText="Regular expression to match the observation's description"
                />
                <TextInputWide
                    source="origin_component_name_version"
                    label="Origin component name:version"
                    helperText="Regular expression to match the component name:version"
                />
                <TextInputWide
                    source="origin_docker_image_name_tag"
                    label="Origin docker image name:tag"
                    helperText="Regular expression to match the docker image name:tag"
                />
                <TextInputWide
                    source="origin_endpoint_url"
                    label="Origin endpoint URL"
                    helperText="Regular expression to match the endpoint URL"
                />
                <TextInputWide
                    source="origin_service_name"
                    label="Origin service name"
                    helperText="Regular expression to match the service name"
                />
                <TextInputWide
                    source="origin_source_file"
                    label="Origin source file"
                    helperText="Regular expression to match the source file"
                />
                <TextInputWide
                    source="origin_cloud_qualified_resource"
                    label="Origin cloud qualified resource"
                    helperText="Regular expression to match the qualified resource name"
                />
                <AutocompleteInputMedium source="new_severity" choices={OBSERVATION_SEVERITY_CHOICES} />
                <AutocompleteInputMedium source="new_status" choices={OBSERVATION_STATUS_CHOICES} />
                <BooleanInput source="enabled" defaultValue={true} />
            </SimpleForm>
        </Edit>
    );
};

const requiredValidate = [required()];

export default GeneralRuleEdit;

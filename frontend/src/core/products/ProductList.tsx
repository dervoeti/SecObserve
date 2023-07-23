import { Fragment } from "react";
import {
    BulkDeleteButton,
    CreateButton,
    Datagrid,
    List,
    NullableBooleanInput,
    ReferenceInput,
    TextField,
    TextInput,
    TopToolbar,
} from "react-admin";

import { PERMISSION_PRODUCT_CREATE } from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import ObservationsCountField from "../../commons/custom_fields/ObservationsCountField";
import { SecurityGateTextField } from "../../commons/custom_fields/SecurityGateTextField";
import { AutocompleteInputMedium } from "../../commons/layout/themes";

const listFilters = [
    <TextInput source="name" alwaysOn />,
    <ReferenceInput source="product_group" reference="product_groups" sort={{ field: "name", order: "ASC" }} alwaysOn>
        <AutocompleteInputMedium optionText="name" />
    </ReferenceInput>,
    <NullableBooleanInput source="security_gate_passed" alwaysOn />,
];

const BulkActionButtons = () => (
    <Fragment>
        <BulkDeleteButton mutationMode="pessimistic" />
    </Fragment>
);

const ListActions = () => {
    const user = localStorage.getItem("user");
    return (
        <TopToolbar>
            {user && JSON.parse(user).permissions.includes(PERMISSION_PRODUCT_CREATE) && <CreateButton />}
        </TopToolbar>
    );
};

const ProductList = () => {
    return (
        <List
            perPage={25}
            pagination={<CustomPagination />}
            filters={listFilters}
            sort={{ field: "name", order: "ASC" }}
            actions={<ListActions />}
            disableSyncWithLocation={false}
        >
            <Datagrid size="medium" rowClick="show" bulkActionButtons={<BulkActionButtons />}>
                <TextField source="name" />
                <TextField source="product_group_name" label="Product Group" />
                <SecurityGateTextField />
                <TextField source="repository_default_branch_name" label="Default branch" sortable={false} />
                <ObservationsCountField withLabel={false} />
            </Datagrid>
        </List>
    );
};

export default ProductList;

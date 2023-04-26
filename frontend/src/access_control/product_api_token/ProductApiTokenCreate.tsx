import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Stack, TextField } from "@mui/material";
import { useState } from "react";
import { SaveButton, SimpleForm, Toolbar, required, useNotify, useRefresh } from "react-admin";

import CopyToClipboardButton from "../../commons/custom_fields/CopyToClipboardButton";
import { AutocompleteInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";
import { ROLE_CHOICES } from "../types";

type CreateProductApiTokenProps = {
    product: any;
};

const CreateProductApiToken = (props: CreateProductApiTokenProps) => {
    const refresh = useRefresh();
    const notify = useNotify();

    const [roleOpen, setRoleOpen] = useState(false);
    const handleRoleOpen = () => setRoleOpen(true);
    const handleRoleClose = () => setRoleOpen(false);

    const [apiToken, setApiToken] = useState("undefined");

    const [showApiTokenOpen, setShowApiTokenOpen] = useState(false);
    const handleApiTokenOpen = () => setShowApiTokenOpen(true);
    const handleApiTokenClose = () => {
        setApiToken("undefined");
        setShowApiTokenOpen(false);
        refresh();
    };

    const CancelButton = () => (
        <Button
            sx={{
                mr: "1em",
                direction: "row",
                justifyContent: "center",
                alignItems: "center",
                color: "#000000dd",
            }}
            variant="contained"
            onClick={handleRoleClose}
            color="inherit"
            startIcon={<CancelIcon />}
        >
            Cancel
        </Button>
    );

    const CustomToolbar = () => (
        <Toolbar sx={{ display: "flex", justifyContent: "flex-end" }}>
            <CancelButton />
            <SaveButton label="Create" icon={<AddIcon />} />
        </Toolbar>
    );

    const handleApiTokenCreate = async (data: any) => {
        const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/product_api_tokens/";
        const create_data = {
            id: props.product.id,
            role: data.role,
        };

        httpClient(url, {
            method: "POST",
            body: JSON.stringify(create_data),
        })
            .then((result) => {
                setApiToken(result.json.token);
                handleApiTokenOpen();
                notify("Product API token created", {
                    type: "success",
                });
            })
            .catch((error) => {
                notify(error.message, {
                    type: "warning",
                });
            });

        setRoleOpen(false);
    };

    return (
        <>
            <Button
                variant="contained"
                onClick={handleRoleOpen}
                sx={{ mr: "7px", width: "fit-content", fontSize: "0.8125rem" }}
                startIcon={<AddIcon />}
            >
                Create API token
            </Button>
            <Dialog open={roleOpen} onClose={handleRoleClose}>
                <DialogTitle>Create product API token</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={handleApiTokenCreate} toolbar={<CustomToolbar />}>
                        <AutocompleteInputWide source="role" choices={ROLE_CHOICES} validate={requiredValidate} />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
            <Dialog open={showApiTokenOpen} onClose={handleApiTokenClose}>
                <DialogTitle>{"Product API token"}</DialogTitle>
                <DialogContent>
                    <Stack direction="row" spacing={2} justifyContent="center" alignItems="center">
                        <TextField disabled defaultValue={apiToken} sx={{ width: "50ch" }} />
                        <CopyToClipboardButton text={apiToken} />
                    </Stack>
                    <br />
                    <br />
                    Make sure to copy the token now. You won&apos;t be able to see it again!
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleApiTokenClose}>OK</Button>
                </DialogActions>
            </Dialog>
        </>
    );
};

const requiredValidate = [required()];

export default CreateProductApiToken;
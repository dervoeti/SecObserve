import DeleteIcon from "@mui/icons-material/Delete";
import { useState } from "react";
import { Button, Confirm, useDelete, useNotify, useRefresh } from "react-admin";

type BranchDeleteProps = {
    branch: any;
};

const BranchDelete = (props: BranchDeleteProps) => {
    const [open, setOpen] = useState(false);
    const [deleted, setDeleted] = useState(false);
    const [error_shown, setErrorShown] = useState(false);
    const [deleteOne, { isLoading, error }] = useDelete(); // eslint-disable-line @typescript-eslint/no-unused-vars
    // isLoading is not needed but easier to let it there
    const refresh = useRefresh();
    const notify = useNotify();
    const handleClick = () => setOpen(true);
    const handleDialogClose = () => setOpen(false);

    const handleConfirm = async () => {
        deleteOne("branches", { id: props.branch.id });
        setDeleted(true);
        refresh();
        setOpen(false);
    };

    if (error && !error_shown) {
        setErrorShown(true);
        setDeleted(false);
        notify("Branch could not be deleted: " + error, {
            type: "warning",
        });
    } else if (deleted) {
        setDeleted(false);
        notify("Branch deleted");
    }

    return (
        <>
            <Button label="Delete" onClick={handleClick} startIcon={<DeleteIcon />} sx={{ color: "#d32f2f" }} />
            <Confirm
                isOpen={open}
                title="Delete branch"
                content={
                    "Are you sure you want to delete the branch " + props.branch.name + " and all of its observations?"
                }
                onConfirm={handleConfirm}
                onClose={handleDialogClose}
            />
        </>
    );
};

export default BranchDelete;

import {Modal, Typography, Form, Input, Button} from "antd";

const {Title} = Typography;

function AddUserModal({open, onClose, onSubmit}) {
    const [form] = Form.useForm();
    const check = () => {
        let data = form.getFieldsValue();
        console.log(data);
        onSubmit(data);
        form.resetFields()

    }
    return (
        <Modal open={open} onCancel={onClose} onOk={form.submit} okText={'Create'} footer={[
            <Button onClick={onClose} color={"danger"} variant={"solid"}>Cancel</Button>,
            <Button onClick={form.submit} color={"cyan"} variant={"solid"}>Create</Button>
        ]}>
            <Title level={2}>Add user</Title>
            <Form layout={"vertical"} form={form} onFinish={check}>
                <Form.Item label={"Name"} name={"name"} rules={[{required: true, message: "Please enter your name"}]}>
                    <Input placeholder={"user name"}></Input>
                </Form.Item>

                <Form.Item label={"Surname"} name={"surname"} rules={[{required: true, message: "Please enter your surname"}]}>
                    <Input placeholder={"Surname name"}></Input>
                </Form.Item>
            </Form>
        </Modal>
    )
}

export default AddUserModal;
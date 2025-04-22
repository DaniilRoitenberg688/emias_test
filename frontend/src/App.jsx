import {useEffect, useState} from 'react'
import './App.css'
import {Table, Button, Flex, Popconfirm, message, Input, Form} from "antd";
import {
    PlusOutlined,
    ReloadOutlined,
    DeleteOutlined,
    EditOutlined,
    CheckOutlined,
    CloseOutlined
} from "@ant-design/icons"
import AddUserModal from "./components/AddUserModal"
import {getUsers, createUser, deleteUser, editUser} from "./api/api.js";


function ChangeCell({s}) {
    console.log(s)
    return (

        <>
            <td><Input></Input></td>
        </>
    )
}

function App() {
    const [messageApi, contextHolder] = message.useMessage();
    const [userToEdit, setUserToEdit] = useState({});
    const columns = [// {title: 'ID', dataIndex: 'id', key: 'id'},
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            align: 'center',
            render: (text, record, index) => {
                if (record.id === userToEdit.id) {
                    form.setFieldValue("name", record.name);
                    return <Form.Item name={"name"} rules={[{required: true, message: "name is required"}]}><Input value={record.name}></Input></Form.Item>
                } else {
                    return text
                }
            },
            width: "40%"

        },
        {
            title: 'Surname',
            dataIndex: 'surname',
            key: 'surname',
            align: 'center',
            render: (text, record, index) => {
                if (record.id === userToEdit.id) {
                    form.setFieldValue("surname", record.surname);
                    return <Form.Item name={"surname"} rules={[{required: true, message: "surname is required"}]}><Input value={record.surname} ></Input></Form.Item>
                } else {
                    return text
                }
            },

        },
        {
            title: 'Delete',
            dataIndex: 'delete',

            render: (_, record) => (
                <Popconfirm title={"Delete?"} onConfirm={() => {
                    confirmDelete(record)
                }}>
                    <Button variant={"filled"} color={"danger"}><DeleteOutlined/></Button>
                </Popconfirm>
            ),
            align: 'center',
            width: "10%"

        },
        {
            title: 'Edit',
            dataIndex: 'edit',

            render: (_, record, index) => {

                if (!userToEdit.id) {
                    console.log('sigma')
                    return <><Button variant={"filled"} color={"yellow"} onClick={() => {
                        setUserInEditing(record, index)
                    }}><EditOutlined/></Button>
                    </>
                } else {
                    if (record.id === userToEdit.id) {
                        return <><Button variant={"filled"} color={"green"}
                                         style={{marginRight: "10px"}} onClick={form.submit}><CheckOutlined/></Button>
                            <Button variant={"filled"} color={"red"} onClick={() => {
                                setUserToEdit({})
                            }}><CloseOutlined/></Button>
                        </>
                    } else {
                        return <Button variant={"filled"} color={"yellow"} disabled={true}><EditOutlined/></Button>
                    }

                }
            },
            align: 'center',
            width: "10%"

        }

    ];


    const [users, setUsers] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [form] = Form.useForm();

    // useEffect(() => {
    //     const loadData = async () => {
    //         try {
    //             console.debug(`Fetching data from endpoint: ${endPoint}`);
    //             const response = await fetch(`${import.meta.env.VITE_APP_API_URL}/get/${endPoint}`);
    //             if (response.ok) {
    //                 const data = await response.json();
    //                 console.debug('Fetched JSON data:', data);
    //                 setJsonData(data);
    //             } else {
    //                 console.error('HTTP error', response.status);
    //             }
    //         } catch (error) {
    //             console.error('Error:', error);
    //         }
    //     };
    //     loadData().catch(error => {
    //         console.error("Unhandled error:", error);
    //     });
    // }, [endPoint]);

    const loadUsers = async () => {
        setIsLoading(true)
        let data = await getUsers();
        setUsers(data);
        console.log(data)
        setIsLoading(false)
    }

    useEffect(() => {
        loadUsers().catch(error => {
            console.log(error)
        });
    }, [])

    const confirmDelete = async record => {
        await deleteUser(record.id)
        let newData = users.filter(item => item.id !== record.id);
        setUsers(newData);
        console.log("sigma")
        messageApi.open({
            type: "success",
            content: "Deleted successfully",


        });

    }

    const setUserInEditing = (record, index) => {
        setUserToEdit(record);
        let newUsers = users;
        console.log(newUsers[index].name)
        setUsers(newUsers)
    }

    const saveUser = async () => {
        let usersNew = users
        let index = users.indexOf(users.filter(item => item.id === userToEdit.id)[0])
        usersNew[index].name = form.getFieldsValue().name
        usersNew[index].surname = form.getFieldsValue().surname
        await editUser(usersNew[index].id, {name: usersNew[index].name, surname: usersNew[index].surname})
        setUsers(usersNew);
        setUserToEdit({})
    }

    const createNew = async (data) => {
        let newUsers = users;
        let user = await createUser(data);
        newUsers.push(user);
        setUsers(newUsers);
        console.log(newUsers)
        setIsModalOpen(false);
        messageApi.open({
            type: "success",
            content: "Created successfully",
        })
    }

    // const mergedColumns = columns.map(col => {
    //     if (!col.editable) {
    //         return col;
    //     }
    //     return Object.assign(Object.assign({}, col), {
    //         onCell: record => ({
    //             record,
    //             s: 'sigma'
    //         }),
    //     });
    // });


    return (
        <>
            {contextHolder}
            <Flex gap={"middle"} style={{margin: "20px"}}>
                <Button size={"large"} color="cyan" variant={"solid"} shape={"circle"}
                        style={{}} onClick={loadUsers}>
                    <ReloadOutlined/>
                </Button>
                <Button size={"large"} color="cyan" variant={"solid"} shape={"circle"}
                        style={{}} onClick={() => setIsModalOpen(true)}>
                    <PlusOutlined/>
                </Button>
            </Flex>
            <Form form={form} onFinish={saveUser}>
                <Table size={"large"} columns={columns} dataSource={users} rowKey={'id'} pagination={false}
                       bordered={true}
                       loading={isLoading}></Table>
            </Form>
            <AddUserModal open={isModalOpen} onClose={() => setIsModalOpen(false)}
                          onSubmit={createNew}/>

        </>

    )
}

export default App

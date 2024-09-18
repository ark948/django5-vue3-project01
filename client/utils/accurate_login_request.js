// this login function is completely ok

const handleSubmit = async (e) => {
    e.preventDefault()

    // validation
    const { email, password } = logindata
    if (!email || !password) {
        responseMessage.value = "Both values are required."
        return
    }

    api.post('auth/login/', { email: email, password: password})
        .then(response => {
            console.log(response.status) // 200
            console.log(response.data.access_token)
            if (response.status === 200) {
                // double checking status code
                user.email = response.data.email
                user.full_name = response.data.full_name
                localStorage.setItem("user", JSON.stringify(user))
                localStorage.setItem("access", JSON.stringify(response.data.access_token))
                localStorage.setItem("refresh", JSON.stringify(response.data.refresh_token))
            }
            notify({
                title: "Welcome",
                text: `${response.data.full_name} have successfully logged in.`
            })
            router.push({ name: "home" })
        })
        .catch(error => {
            if (error.response) console.log("response contains error")
            else if (error.request) console.log("no response")
            else console.log("error in setting up the request")
        })
}
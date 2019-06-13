<template>
        <div class="login">
          <div v-if="proccessing" class="text-center"> Please wait... </div>
          <div v-if="message" class="text-center"> {{message}} </div>

          <b-form-input
            v-model="username"
            type="text"
            class="input-form"
            placeholder="Username">
          </b-form-input>

          <b-form-input
            v-model="password"
            class="input-form"
            type="password"
            placeholder="Password">
          </b-form-input>

          <b-button 
            v-on:click="login" 
            variant="primary" 
            class="btn-block"
          >
          LOG IN
         </b-button>
         <b-button 
            v-on:click="register"  
            class="btn-block register"
          >
          SIGN UP
         </b-button>
        </div>
    </template>


    <script>
    export default {
      name: "Login",
      data() {
        return {
          username: "",
          password: "",
          proccessing: false,
          message: ""
        };
      },
      methods: {
        register:function(){
          window.location.href = 'http://localhost:5000/api/register';
        },
        login: function() {
          this.loading = true;
          this.axios
            .post("/api/login", {
              username: this.username,
              password: this.password
            })
            .then(response => {
              if (response.data.status == "success") {
                this.proccessing = false;
                this.$emit("authenticated", true, response.data.data);
              } else {
                this.message = "Login Failed, try again";
              }
            })
            .catch(error => {
              this.message = "Login Failed, try again";
              this.proccessing = false;
            });
        }
      }
    };
    </script>

    <style scoped>
    .login {
      width: 500px;
      border: 1px solid #007bff;
      background-color: #ffffff;
      margin: auto;
      margin-top: 200px;
      padding: 20px;
    }
    .input-form {
      margin-bottom: 9px;
    }
    .register{
      background-color: #007bff !important;
      border: 1px solid #007bff;
    }
    </style>
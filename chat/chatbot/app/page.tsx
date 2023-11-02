'use client'

import { useState } from 'react'

const message : any = (text: string, botMessage: boolean) => {
  if(botMessage){
    return(
      <div className="flex w-full mt-2 space-x-3 max-w-xs">
        <div className="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300"></div>
        <div>
          <div className="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
            <p className="text-sm">{text}</p>
          </div>
        </div>
      </div>
    )
  }else{
    return(
      <div className="flex w-full mt-2 space-x-3 max-w-xs ml-auto justify-end">
        <div>
          <div className="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
            <p className="text-sm">{text}</p>
          </div>
        </div>
        <div className="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300"></div>
      </div>
    )
  }
}

const startMessages : any = [
  message("¡Bienvenido! ¿Qué deseas hacer? Puedes:", true),
  message(" 1. Loggearte con: /login USERNAME PASSWORD", true),
  message(" 2. Una vez loggeado, puedes ver tu granja con: /show", true)
]

export default function Home() {
  
  const [input, setInput] = useState("")
  const [token, setToken] = useState("-1")
  const [messages, setMessages] = useState(startMessages)

  function handleSubmit() {

    const data = input.split(" ");
    const action = data[0]
    
    if(action === "/login"){

      console.log("[LOGGING]")

      if(!data[1] || !data[2]){
        console.log("No username or password")
        setMessages([...messages, message(input, false), message("Usuario o contraseña no ingresados.", true)])
        return
      }

      const username = data[1]
      const password = data[2]

      fetch("https://login_service/login", {
        method: "POST",
        body: JSON.stringify({
          username: username,
          password: password
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      }).then((response) => {
        console.log(response)
        setMessages([...messages, message(input, false), message("Bienvenido!", true)])
      }).catch((error) => {
        setMessages([...messages, message(input, false), message("Problema con los servidores de usuario...", true)])
      })
    } else if(action === "/show"){
      if(token === "-1"){
        setMessages([...messages, message(input, false), message("Debe loggearse para poder visualizar su granja.", true)])
      }else{
        fetch("https://render_service/farms/" + token, {
          method: "GET"
        }).then((response) => {
          console.log(response)
          setMessages([...messages, message(input, false), message("Imagen recibida!", true)])
        }).catch((error) => {
          setMessages([...messages, message(input, false), message("Problema con los servidores de render...", true)])
        })
      }
    } else {
        setMessages([...messages, message(input, false), message("No te entiendo.", true)])
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="flex flex-col items-center justify-center w-screen min-h-screen bg-gray-100 text-gray-800 p-10">
        <div className="flex flex-col flex-grow w-full max-w-xl bg-white shadow-xl rounded-lg overflow-hidden">
          <div className="flex flex-col flex-grow h-0 p-4 overflow-auto">
            {messages}
          </div>
          
          <div className="bg-gray-300 p-4">
            <input className="flex items-center h-10 w-full rounded px-3 text-sm" type="text" placeholder="Type your message…" onChange={(e) => {setInput(e.target.value); console.log(input)}}/>
            <input className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" type='submit' value="Enviar" onClick={handleSubmit}/>
          </div>
        </div>
      </div>
    </main>
  )
}

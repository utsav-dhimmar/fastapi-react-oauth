import { useState } from 'react'
import './App.css'
import { GoogleLogin } from './components/GoogleLogin';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className='hero'>
        <button onClick ={() => setCount((count) => count + 1)}>
          Click Me {count}
        </button>
        <GoogleLogin/>
      </div>
    </>
  )
}

export default App

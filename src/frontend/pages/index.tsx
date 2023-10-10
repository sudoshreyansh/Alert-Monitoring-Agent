import Image from 'next/image'
import { Inter } from 'next/font/google'
import { FaLocationDot, FaCirclePlus } from 'react-icons/fa6'

const inter = Inter({ subsets: ['latin'] })

function UserInput() {
  
}

export default function Home() {
  return (
    <main className={`text-white min-h-screen relative ${inter.className}`}>
      <div className='absolute left-0 top-0 right-0 bottom-0 -z-10'>
        <Image
          src="/background.jpg"
          alt=""
          fill={true}
          style={{
            objectFit: 'cover',
          }}
          />
      </div>
      <div className='max-w-lg mx-auto min-h-screen'>
        <div className='flex justify-between py-5 text-lg'>
          <div className='cursor-pointer'>
            <FaLocationDot />
          </div>
          <div className='cursor-pointer'>
            <FaCirclePlus />
          </div>
        </div>
        <div className='h-60'>
          <div className='text-2xl font-medium my-4'>
            London, UK
          </div>
        </div>
        <div className='mb-4'>
          <span className='text-8xl font-medium'>
            26
          </span>
          <span className='text-8xl inline-block -mr-9 ml-2.5'>
            &deg;
          </span>
          <span className='text-2xl font-medium'>
            Few Clouds
          </span>
        </div>
        <div className='text-lg font-medium'>
          Tue &nbsp; 30&deg; / 20&deg;
        </div>
        <div className='text-lg font-medium mb-4'>
          Feels Like: 28.4&deg;
        </div>
      </div>
    </main>
  )
}

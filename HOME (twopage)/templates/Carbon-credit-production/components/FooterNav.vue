<template>
    <footer class="bg-gray-800 pt-3 sm:mt-10">
        <div class="max-w-6xl m-auto text-gray-800 flex flex-wrap justify-center">
            <!-- Col-1 -->
            <div class=" hidden p-5 w-1/1 sm:w-4/12 md:w-3/12 text-center">
                <!-- Col Title -->
                <div class="text-xs uppercase text-gray-400 font-medium mb-6">
                    {{ $t('footer.title.how_to')}}
                </div>

                <!-- Links -->
                <a href="#" class="my-3 block text-gray-300 hover:text-gray-100 text-sm font-medium duration-700">
                    {{ $t('footer.link.register_pilot') }}
                </a>
                <a href="#" class="my-3 block text-gray-300 hover:text-gray-100 text-sm font-medium duration-700">
                    {{ $t('footer.link.register_UAS') }}
                </a>
                
            </div>

            <!-- Col-2 -->
            <div class=" hidden p-5 w-1/1 sm:w-4/12 md:w-3/12 text-center">
                <!-- Col Title -->
                <div class="text-xs uppercase text-gray-400 font-medium mb-6">
                    {{ $t('button.download') }}
                </div>
                <!-- Links -->
                <a href="#" class="my-3 block text-gray-300 hover:text-gray-100 text-sm font-medium duration-700">
                    {{ $t('footer.link.document_for_registration') }}
                </a>
               
            </div>

            <!-- Col-3 -->
            <div class="hidden p-5 w-1/1 sm:w-4/12 md:w-3/12 text-center">
                <!-- Col Title -->
                <div class="text-xs uppercase text-gray-400 font-medium mb-6">
                    {{ $t('footer.title.must_know')}}
                </div>
                <!-- Links -->
                <a href="#" class="my-3 block text-gray-300 hover:text-gray-100 text-sm font-medium duration-700">
                    {{ $t('footer.link.type_of_legel_entity') }}
                </a>
                <a href="#" class="my-3 block text-gray-300 hover:text-gray-100 text-sm font-medium duration-700">
                    {{ $t('footer.link.type_of_drone_register') }}
                </a>
                
            </div>

            <!-- Col-3 -->
            <div class="hidden p-5 w-1/1 sm:w-4/12 md:w-3/12 text-center">
                <!-- Col Title -->
                <div class="text-xs uppercase text-gray-400 font-medium mb-6">
                    Community
                </div>
                <!-- Links -->
                <a href="#" class="my-3 block text-gray-300 hover:text-gray-100 text-sm font-medium duration-700">
                    Facebook
                </a>
                <a href="#" class="my-3 block text-gray-300 hover:text-gray-100 text-sm font-medium duration-700">
                    Youtube
                </a>
            </div>
        </div>

        <div v-show="false" class=" justify-center items-center space-y-4 sm:flex sm:space-y-0 sm:space-x-4 mb-6 mx-6 mt-4">
			<a href="#" class="w-full sm:w-auto bg-gray-800 hover:bg-gray-700 focus:ring-4 focus:ring-gray-300 text-white rounded-lg inline-flex items-center justify-center px-4 py-2.5 dark:bg-gray-700 dark:hover:bg-gray-600 dark:focus:ring-gray-700 border-gray-500 border">
				<svg class="mr-3 w-7 h-7" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="apple" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
					<path fill="currentColor" d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"></path>
				</svg>
				<div class="text-left">
					<div class="mb-1 text-xs">Download on the</div>
					<div class="-mt-1 font-sans text-sm font-semibold">Mac App Store</div>
				</div>
			</a>
			<a href="#" class="w-full sm:w-auto bg-gray-800 hover:bg-gray-700 focus:ring-4 focus:ring-gray-300 text-white rounded-lg inline-flex items-center justify-center px-4 py-2.5 dark:bg-gray-700 dark:hover:bg-gray-600 dark:focus:ring-gray-700 border-gray-500 border">
				<svg class="mr-3 w-7 h-7" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="google-play" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
					<path fill="currentColor" d="M325.3 234.3L104.6 13l280.8 161.2-60.1 60.1zM47 0C34 6.8 25.3 19.2 25.3 35.3v441.3c0 16.1 8.7 28.5 21.7 35.3l256.6-256L47 0zm425.2 225.6l-58.9-34.1-65.7 64.5 65.7 64.5 60.1-34.1c18-14.3 18-46.5-1.2-60.8zM104.6 499l280.8-161.2-60.1-60.1L104.6 499z"></path>
				</svg>
				<div class="text-left">
					<div class="mb-1 text-xs">Get in on</div>
					<div class="-mt-1 font-sans text-sm font-semibold">Google Play</div>
				</div>
			</a>
		</div>


        <!-- Copyright Bar -->
        <div class="pt-2">
            <div class="flex justify-center pb-5 px-3 m-auto pt-5 border-t border-gray-500 text-gray-400 text-sm flex-col md:flex-row max-w-6xl">
                <div class="mt-2 text-center">
                    Copyright © 2022 DELVAEROSPACE. All Rights Reserved. Developed by <a href="https://delvaerospace.com" class="hover:text-caat-100" target="_blank">DELVAEROSPACE</a>
                </div>

              
            </div>
        </div>
    </footer>
</template>
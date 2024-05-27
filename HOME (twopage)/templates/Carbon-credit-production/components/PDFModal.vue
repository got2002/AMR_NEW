<template>
	<div class="modal fixed w-full h-full top-0 left-0 flex items-center justify-center" style="z-index: 99999">
		<div class="modal-overlay absolute w-full h-full bg-black opacity-60"></div>

		<div class="modal-container fixed w-full h-full z-50 overflow-y-auto">
			<div class="modal-close absolute top-0 right-0 cursor-pointer flex flex-col items-center mt-2 mr-4 text-red-500 shadow-lg z-50 bg-white rounded" @click="$emit('close')">
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
					<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
				</svg>
			</div>
			<div class="modal-content container mx-auto mt-14 h-auto text-left bg-gray-500 rounded-lg shadow-lg">
				<vue-pdf style="height: 90vh" :pdf="pdfURL" :config="pdfConfig"></vue-pdf>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		props: ["pdfURL"],
		data() {
			return {
				pdfConfig: {
					sidebar: {
						viewThumbnail: true,
						viewOutline: true,
						viewAttachments: true,
					},
					secondaryToolbar: {
						secondaryPresentationMode: true,
						secondaryOpenFile: false,
						secondaryPrint: true,
						secondaryDownload: true,
						secondaryViewBookmark: false,
						firstPage: true,
						lastPage: true,
						pageRotateCw: true,
						pageRotateCcw: true,
						cursorSelectTool: true,
						cursorHandTool: true,
						scrollVertical: true,
						scrollHorizontal: true,
						scrollWrapped: true,
						spreadNone: true,
						spreadOdd: true,
						spreadEven: true,
						documentProperties: false,
					},
					toolbar: {
						toolbarViewerLeft: {
							findbar: true,
							previous: true,
							next: true,
							pageNumber: false,
						},
						toolbarViewerRight: {
							presentationMode: true,
							openFile: false,
							print: false,
							download: true,
							viewBookmark: false,
						},
						toolbarViewerMiddle: {
							zoomOut: true,
							zoomIn: true,
							scaleSelectContainer: true,
						},
					},
					errorWrapper: true,
				},
			};
		},
	};
</script>

<style></style>

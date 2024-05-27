<template>
	<td
		class="border-t-0 px-1 whitespace-nowrap align-center"
		:class="{
			'text-left': align === 'left',
			'text-center': align === 'center',
			'text-right': align === 'right',
		}"
	>
		<span class="px-3 py-1 rounded-full shadow-sm" :class="{
            'bg-yellow-100 bg-opacity-40 border border-yellow-500 text-yellow-500':status === 0,
            'bg-blue-100 bg-opacity-40 border border-blue-500 text-blue-500':status === 1,
            'bg-green-100 bg-opacity-40 border border-green-500 text-green-500':status === 2,
            'bg-red-100 bg-opacity-40 border border-red-500 text-red-500':status === 3 || status === 5,
            'bg-gray-100 bg-opacity-40 border border-gray-500 text-gray-500':status === 4,

        

        }">
			{{ statusText(status) }}
		</span>
	</td>
</template>

<script>
	export default {
        props:['status','align'],
        methods:{
            statusText(status){
                switch (status) {
                    case 0:
                        if(this.$i18n.locale === 'th') return 'รอดำเนินการ'
                        else return 'pending'
                    case 1:
                        if(this.$i18n.locale === 'th') return 'กำลังดำเนินการโอน'
                        else return 'in-progress'
                    case 2:
                        if(this.$i18n.locale === 'th') return 'โอนสำเร็จ'
                        else return 'completed'
                    case 3:
                        if(this.$i18n.locale === 'th') return 'โอนไม่สำเร็จ'
                        else return 'failed'
                    case 4:
                        if(this.$i18n.locale === 'th') return 'ยกเลิกการโอน'
                        else return 'cancelled'
                    case 5:
                        if(this.$i18n.locale === 'th') return 'ปฏิเสธการโอน'
                        else return 'rejected'
                       
                
                    default:
                        break;
                }
            }
        }
    };
</script>

<style></style>

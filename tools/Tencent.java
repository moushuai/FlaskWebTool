import com.qcloud.*;

import java.awt.Image;
import java.io.*;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

public class Tencent {
	// appid, access id, access key apply at http://app.qcloud.com
	public static final int APP_ID_V1 = 201437;
	public static final String SECRET_ID_V1 = "AKIDblLJilpRRd7k3ioCHe5JGmSsPvf1uHOf";
	public static final String SECRET_KEY_V1 = "6YvZEJEkTGmXrtqnuFgjrgwBpauzENFG";
        
    public static final int APP_ID_V2 = 10011383;
	public static final String SECRET_ID_V2 = "AKIDqKpES8T0vk4vwTjfYU0cElKMfAUxnLE0";
	public static final String SECRET_KEY_V2 = "56cxQtM5OQ91nnIAjoamIfGOFJI3n1wD";
    public static final String BUCKET = "porndector";        //bucket name
        
    public static final String TEST_URL = "http://porndector-10011383.image.myqcloud.com/0506af6a-188c-4dd6-bbb5-48dc53963831";
    public static final String FOLD_PATH = "D:/SMU/PornDetector/video/normal";
    public static final String RESULT_FOLD = "D:/SMU/PornDetector/ResultNormalTencent/";
    public static final String FILE_HEADER = "IMAGE_NAME	RESULT	CONFIDENCE	PORN_SCORE	NORMAL_SCORE	HOT_SCORE";
	public static void main(String[] args) throws Exception {

		Map<String, Map<String, String>> resultMap = null;
		resultMap = pornDetect();
		writeToFile(resultMap);
	}
	
    public static Map<String, Map<String, String>> pornDetect(){
    	Map<String, Map <String, String>> resultMap = new HashMap<String, Map<String, String>>();
    	Map<String, String> vedioMap = null;
    	PicCloud pc = new PicCloud(APP_ID_V2, SECRET_ID_V2, SECRET_KEY_V2, BUCKET);
//    	PornDetectInfo info = new PornDetectInfo();
		File fold = new File(FOLD_PATH);
		if(fold.isDirectory()){
			for(File video : fold.listFiles()){
				System.out.println(video.toString());
				vedioMap = new HashMap<String, String>();
				if(video.isDirectory()){
					for(String img : video.list()){
						UploadResult result = new UploadResult();
						int uploadRet = pc.upload(video.toString() + "/" + img, result);
						if (uploadRet == 0) {
//							System.out.println("upload pic success");
							PornDetectInfo info = new PornDetectInfo();
							int pornRet = pc.pornDetect(result.downloadUrl, info);
							String str = info.result + " " + info.confidence + " " 
									+ info.pornScore + " " + info.normalScore + " "
									+ info.hotScore;
							System.out.println(img + " " + str);
							vedioMap.put(img, str);

							
						} else {
							System.out.println("upload pic error, error=" + pc.getError());
						}
					}
					resultMap.put(video.toString().substring(video.toString().lastIndexOf("\\") + 1), vedioMap);
				}
			}
		}else{
			System.out.println("error : is not a fold path!");
			return null;
		}
		return resultMap;
    }
    
    public static boolean writeToFile(Map<String, Map<String, String>> resultMap) throws IOException{
    	for(Entry<String, Map<String, String>> entry : resultMap.entrySet()){
    		
    		File file = new File(RESULT_FOLD + entry.getKey() + ".txt");
    		System.out.println(file.toString());
    		if(!file.exists())
    			file.createNewFile();
        	FileWriter fw = new FileWriter(file);
        	fw.write(FILE_HEADER);
    		for(Entry<String, String> entry2 : entry.getValue().entrySet()){
    			fw.write("\r\n"+entry2.getKey() + "	" + entry2.getValue());
    		}
    		fw.close();
    	}
    	
    	return true;
    }
        
    public static void signTest() {
        PicCloud pc = new PicCloud(APP_ID_V2, SECRET_ID_V2, SECRET_KEY_V2, BUCKET);
        long expired = System.currentTimeMillis() / 1000 + 3600;
        String sign = pc.getSign(expired);
        System.out.println("sign="+sign);
        
    }
    
    public static void picV1Test(String pic) throws Exception {
        PicCloud pc = new PicCloud(APP_ID_V1, SECRET_ID_V1, SECRET_KEY_V1);
        picBase(pc, pic);
    }
    
    public static void picV2Test(String pic) throws Exception {
        PicCloud pc = new PicCloud(APP_ID_V2, SECRET_ID_V2, SECRET_KEY_V2, BUCKET);
        picBase(pc, pic);
    }

	public static void picBase(PicCloud pc, String pic) throws Exception {
		UploadResult result = new UploadResult();
		UploadResult result2 = new UploadResult();
		PicInfo info = new PicInfo();

		// upload a picture
		System.out.println("======================================================");
		int ret = pc.upload(pic, result);
		if (ret == 0) {
			System.out.println("upload pic success");
			result.print();
		} else {
			System.out.println("upload pic error, error=" + pc.getError());
		}

                FileInputStream fileStream = new FileInputStream(pic);
                ret = pc.upload(fileStream, result);
		if (ret == 0) {
			System.out.println("upload pic2 success");
			result.print();
		} else {
			System.out.println("upload pic2 error, error=" + pc.getError());
		}
                  
                FileInputStream fileStream2 = new FileInputStream(pic);
                byte[] data = new byte[fileStream2.available()];
                fileStream2.read(data);
                ByteArrayInputStream inputStream = new ByteArrayInputStream(data);
                ret = pc.upload(inputStream, result);
		if (ret == 0) {
			System.out.println("upload pic3 success");
			result.print();
		} else {
			System.out.println("upload pic3 error, error=" + pc.getError());
		}

		// obtain the state of a picture
		System.out.println("======================================================");
		ret = pc.stat(result.fileId, info);
		if (ret == 0) {
			System.out.println("Stat pic success");
			info.print();
		} else {
			System.out.println("Stat pic error, error=" + pc.getError());
		}

		// copy a picture
		System.out.println("======================================================");
		ret = pc.copy(result.fileId, result2);
		if (ret == 0) {
			System.out.println("copy pic success");
			result2.print();
		} else {
			System.out.println("copy pic error, error=" + pc.getError());
		}     

		// delete a picture
		System.out.println("======================================================");
		//ret = pc.Delete(result.fileid);
		if (ret == 0) {
			System.out.println("delete pic success");
		} else {
			System.out.println("delete pic error, error=" + pc.getError());
		} 
	}
        
        public static void pornTest(String url){
            PicCloud pc = new PicCloud(APP_ID_V2, SECRET_ID_V2, SECRET_KEY_V2, BUCKET);
            PornDetectInfo info = new PornDetectInfo();
            
            int ret = pc.pornDetect(url, info);
            if (ret == 0) {
                System.out.println("detect porn pic success");
		info.print();
            } else {
		System.out.println("detect porn pic error, error=" + pc.getError());
            } 
        }
}
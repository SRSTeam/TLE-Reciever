import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.FileOutputStream;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.CookieHandler;
import java.net.CookieManager;
import java.net.CookiePolicy;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;
import java.util.Properties;

public class tleReciever {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		try {
			// Initializes connection to Space-Track.org:
			Properties prop = new Properties();
			prop.load(new FileInputStream("config.properties"));

			String baseURL = "https://www.space-track.org";
			String authPath = "/auth/login";
			String userName = prop.getProperty("username");
			String password = prop.getProperty("password");	 
			System.out.printf("%s, %s\n" ,userName, password);
			
			CookieManager manager = new CookieManager();
			manager.setCookiePolicy(CookiePolicy.ACCEPT_ALL);
			CookieHandler.setDefault(manager);
			
			URL url = new URL(baseURL+authPath);
			
			HttpsURLConnection conn = (HttpsURLConnection) url.openConnection();
			conn.setDoOutput(true);
			conn.setRequestMethod("POST");

			String input = "identity="+userName+"&password="+password;

			OutputStream os = conn.getOutputStream();
			os.write(input.getBytes());
			os.flush();

			BufferedReader br = new BufferedReader(new InputStreamReader((conn.getInputStream())));

			String output;
			System.out.println("Output from Server .... \n");
			while ((output = br.readLine()) != null) {
				System.out.println(output);
			}

			// START HERE:
			String query = "/basicspacedata/query/class/tle_latest/ORDINAL/1/EPOCH/%3Enow-30/orderby/NORAD_CAT_ID/format/3le";

			url = new URL(baseURL + query);

			br = new BufferedReader(new InputStreamReader((url.openStream())));
			

			while ((output = br.readLine()) != null) {
				System.out.println(output);
			}

			// Logout of Space-Track.org:
			url = new URL(baseURL + "/ajaxauth/logout");
			br = new BufferedReader(new InputStreamReader((url.openStream())));
			conn.disconnect();

		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
package ch.benlegiang.annotation.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {

	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}


	/*server.compression.enabled=true
	server.compression.min-response-size=5KB
	server.compression.mime-types=application/json,application/xml,text/html,text/xml,text/plain
	*/
}

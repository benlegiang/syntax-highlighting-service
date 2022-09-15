package ch.benlegiang.annotation.api;


import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

@Configuration
@EnableAsync
public class ApplicationConfiguration {

    @Bean(name = "cpuBoundThreadPoolTaskExecutor")
    public Executor cpuBoundThreadPoolTaskExecutor() {
        int coreCount = Runtime.getRuntime().availableProcessors();
        return Executors.newFixedThreadPool(1);
    }

}
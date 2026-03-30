package com.nids.nids_backend;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/alerts")
@CrossOrigin(origins = "*")
public class AlertController {

    @Autowired
    private AlertRepository alertRepository;

    // Python sends alert here
    @PostMapping("/add")
    public Alert addAlert(@RequestBody Alert alert) {
        alert.setTimestamp(LocalDateTime.now());
        return alertRepository.save(alert);
    }

    // React fetches all alerts here
    @GetMapping("/all")
    public List<Alert> getAllAlerts() {
        return alertRepository.findAll();
    }

    // Test endpoint
    @GetMapping("/test")
    public String test() {
        return "NIDS Backend is running!";
    }
}
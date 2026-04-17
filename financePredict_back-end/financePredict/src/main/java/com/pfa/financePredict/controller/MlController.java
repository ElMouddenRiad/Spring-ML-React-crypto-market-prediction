package com.pfa.financePredict.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.LinkedHashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/ml")
public class MlController {

    @GetMapping("/btc-next-day")
    public ResponseEntity<?> predictBtcNextDay() {
        try {
            Path backendDir = Paths.get("").toAbsolutePath().normalize();
            Path repoRoot = backendDir.getParent().getParent();
            Path pythonExe = repoRoot.resolve(".venv").resolve("Scripts").resolve("python.exe");
            Path scriptPath = repoRoot.resolve("MachineLearning").resolve("MLModel.py");

            ProcessBuilder pb = new ProcessBuilder(
                    pythonExe.toString(),
                    scriptPath.toString()
            );
            pb.redirectErrorStream(true);

            Process process = pb.start();
            StringBuilder output = new StringBuilder();
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    output.append(line).append(System.lineSeparator());
                }
            }

            int exitCode = process.waitFor();
            if (exitCode != 0) {
                Map<String, Object> error = new LinkedHashMap<>();
                error.put("status", "error");
                error.put("message", "ML script exited with non-zero code");
                error.put("exitCode", exitCode);
                error.put("output", output.toString());
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
            }

            Map<String, String> parsed = parseMlOutput(output.toString());
            Map<String, Object> response = new LinkedHashMap<>();
            response.put("status", "ok");
            response.put("metrics", parsed);
            response.put("rawOutput", output.toString().trim());
            return ResponseEntity.ok(response);

        } catch (Exception ex) {
            Map<String, Object> error = new LinkedHashMap<>();
            error.put("status", "error");
            error.put("message", ex.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }

    private Map<String, String> parseMlOutput(String output) {
        Map<String, String> parsed = new LinkedHashMap<>();
        String[] lines = output.split("\\R");
        for (String line : lines) {
            if (line.contains(":")) {
                String[] kv = line.split(":", 2);
                parsed.put(kv[0].trim(), kv[1].trim());
            }
        }
        return parsed;
    }
}

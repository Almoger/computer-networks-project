# Computer Networks Project

## 👥 Authors
**Students**: Almog Schwartzberg and Eliad Bicher

**Date**: January 2026

## 📌 Project Overview

The project is structured into two main parts:

- TCP/IP Data Encapsulation & Traffic Analysis: Simulating the process of data packaging across network layers and performing packet capture analysis using Wireshark.

- Chat Application: Developing a real-time communication application using TCP sockets, featuring bidirectional messaging along with a full network traffic analysis.

## 📁 Project Structure

| File | Description |
|------|-------------|
| **General Files** ||
| `project_report.docx` | 📄 Comprehensive final report covering methodology, encapsulation analysis, and app architecture |
| **Part 1 - TCP/IP Data Encapsulation & Traffic Analysis** ||
| `group03_http_input.csv` | 📄 CSV with 20 application layer messages (HTTP) |
| `tcp_ip_encapsulation-annotated-v1.ipynb` | 📓 Jupyter notebook for packet encapsulation |
| `packets.pcap` | 📡 Wireshark network capture file containing the analyzed traffic |
| **Part 2 - Chat Application** ||
| `server.py` | 🖥️ Multithreaded TCP server managing client routing via sockets |
| `client.py` | 💬 TCP client interface for real-time messaging |
| `server-client-messages.pcap` | 📡 Wireshark network capture file containing the application's analyzed traffic |

## 📂 Part 1: TCP/IP Data Encapsulation & Traffic Analysis

We analyzed TCP/IP data encapsulation and packet capture. We prepared a CSV file of application messages using AI for content generation. Using the Jupyter Notebook, we simulated the encapsulation process and captured the traffic with Wireshark to analyze the network results.

## 📂 Part 2: Chat Application

We developed a multi-client chat system using Python and TCP sockets. The system uses threads to handle bidirectional communication between multiple clients. We used Wireshark to analyze the communication up to the network layer.

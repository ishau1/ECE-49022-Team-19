// #include <iostream>
// #include <libserialport.h>
// #include <string>
// #include <chrono>
// #include <thread>
// using namespace std;
// using namespace std::chrono;

// sp_return openSerialPort(struct sp_port **port, const char *port_name) 
// {
//     sp_get_port_by_name(port_name, port);
//     if (*port == nullptr) 
//     {
//         cerr << "Error: Cannot find serial port " << port_name << endl;
//         return SP_ERR_FAIL;
//     }
    
//     if (sp_open(*port, SP_MODE_READ_WRITE) != SP_OK) 
//     {
//         cerr << "Error: Unable to open serial port " << port_name << endl;
//         return SP_ERR_FAIL;
//     }

//     sp_set_baudrate(*port, 115200);
//     sp_set_bits(*port, 8);
//     sp_set_parity(*port, SP_PARITY_NONE);
//     sp_set_stopbits(*port, 1);
//     sp_set_flowcontrol(*port, SP_FLOWCONTROL_NONE);
//     return SP_OK;
// }

// // Send data to the ESP32
// void sendSerialData(struct sp_port *port, const string &data) 
// {
//     sp_nonblocking_write(port, data.c_str(), data.length());
// }

// // Read ESP32 output
// void waitForReady(struct sp_port *port, steady_clock::time_point start_time) 
// {
//     string received;
//     while (true) 
//     {
//         char buffer[256];
//         int bytesRead = sp_nonblocking_read(port, buffer, sizeof(buffer) - 1);

//         if (bytesRead > 0) 
//         {
//             buffer[bytesRead] = '\0';
//             received = string(buffer);
//             cout << "ESP32: " << received << endl;

//             if (received.find("READY") != string::npos) 
//             {
//                 auto end_time = steady_clock::now();
//                 auto response_time = duration_cast<milliseconds>(end_time - start_time).count();
//                 cout << "✅ Response Time: " << response_time << " ms" << endl;
//                 return;
//             }
//         }
//         this_thread::sleep_for(chrono::milliseconds(50));  // Prevent CPU overload
//     }
// }

// int main() 
// {
//     const char *portName = "/dev/ttyS3";
//     struct sp_port *port;

//     if (openSerialPort(&port, portName) != SP_OK) 
//     {
//         return 1;
//     }

//     string sequence[] = {"1", "2", "3", "4", "5", "6"};

//     for (int i = 0; i < 5; i++) 
//     {  
//         for (const string &number : sequence) 
//         {
//             auto start_time = steady_clock::now();

//             sendSerialData(port, number + "\n");
//             cout << "Sent: " << number << endl;
//             waitForReady(port, start_time);
//         }
//     }

//     sendSerialData(port, "end\n");
//     cout << "Sent: end" << endl;

//     sp_close(port);
//     sp_free_port(port);
//     cout << "Sequence complete. Exiting program." << endl;
    
//     return 0;
// }

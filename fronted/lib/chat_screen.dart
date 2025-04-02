
// import 'package:flutter/material.dart';
// import 'package:url_launcher/url_launcher.dart';
// import 'package:http/http.dart' as http;
// import 'dart:convert';
// import 'dart:async';
// import 'package:flutter_markdown/flutter_markdown.dart';

// class ChatScreen extends StatefulWidget {
//   const ChatScreen({super.key});

//   @override
//   ChatScreenState createState() => ChatScreenState();
// }

// class ChatScreenState extends State<ChatScreen> with AutomaticKeepAliveClientMixin {
//   final TextEditingController _queryController = TextEditingController();
//   final List<Map<String, dynamic>> messages = [];
//   final ScrollController _scrollController = ScrollController();
//   bool isLoading = false;

//   @override
//   bool get wantKeepAlive => true; // Keeps state alive for performance

//   Future<void> sendQuery() async {
//     String query = _queryController.text.trim();
//     if (query.isEmpty || isLoading) return;

//     setState(() {
//       messages.insert(0, {"sender": "user", "message": query, "type": "text"});
//       _queryController.clear();
//       isLoading = true;
//     });

//     try {
//       var response = await fetchResponse(query); // Removed `compute`

//       if (response["status"] == 200) {
//         setState(() {
//           messages.insert(0, {
//             "sender": "ai",
//             "message": response["message"],
//             "sources": response["sources"] ?? []
//           });
//         });
//       } else {
//         showErrorMessage("Error fetching response.");
//       }
//     } catch (e) {
//       showErrorMessage("An error occurred: $e");
//     } finally {
//       setState(() {
//         isLoading = false;
//       });
//     }
//   }

//   Future<Map<String, dynamic>> fetchResponse(String query) async {
//     final url = Uri.parse("https://commonly-golden-lionfish.ngrok-free.app/ask"); // Updated for emulator
//     final response = await http.post(
//       url,
//       headers: {"Content-Type": "application/json"},
//       body: jsonEncode({"query": query}),
//     );

//     if (response.statusCode == 200) {
//       var jsonResponse = jsonDecode(response.body);
//       return {
//         "status": 200,
//         "message": jsonResponse["response"] ?? "No response",
//         "sources": jsonResponse["sources"] ?? []
//       };
//     }
//     return {"status": response.statusCode, "message": "Error", "sources": []};
//   }

//   void showErrorMessage(String message) {
//     setState(() {
//       messages.insert(0, {"sender": "ai", "message": message, "sources": []});
//     });
//   }

//   void openUrl(String url) async {
//     Uri uri = Uri.parse(url);
//     if (await canLaunchUrl(uri)) {
//       await launchUrl(uri, mode: LaunchMode.externalApplication);
//     } else {
//       ScaffoldMessenger.of(context).showSnackBar(
//         SnackBar(content: Text("Could not open the link: $url")),
//       );
//     }
//   }

//   @override
//   Widget build(BuildContext context) {
//     super.build(context); // Required for keeping state alive

//     return Scaffold(
//       appBar: AppBar(
//         title: const Text("Vizzhy AI Agent", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
//         centerTitle: true,
//         backgroundColor: const Color.fromARGB(221, 91, 153, 240),
//       ),
//       body: Column(
//         children: [
//           Expanded(
//             child: ListView.separated(
//               controller: _scrollController,
//               padding: const EdgeInsets.all(12),
//               reverse: true, // New: Automatically scrolls to the bottom
//               itemCount: messages.length,
//               separatorBuilder: (_, __) => const SizedBox(height: 10),
//               itemBuilder: (context, index) {
//                 final message = messages[index];
//                 final isUser = message["sender"] == "user";

//                 return Column(
//                   crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
//                   children: [
//                     Container(
//                       padding: const EdgeInsets.all(12),
//                       decoration: BoxDecoration(
//                         color: isUser ? Colors.blue : Colors.grey[300],
//                         borderRadius: BorderRadius.circular(12),
//                       ),
//                       child: message["sender"] == "ai"
//                           ? MarkdownBody(
//                               data: message["message"],
//                               selectable: true,
//                               styleSheet: MarkdownStyleSheet.fromTheme(Theme.of(context)).copyWith(
//                                 p: const TextStyle(fontSize: 16),
//                               ),
//                             )
//                           : Text(
//                               message["message"],
//                               style: TextStyle(color: isUser ? Colors.white : Colors.black, fontSize: 16),
//                             ),
//                     ),
//                     if (message.containsKey("sources") && message["sources"].isNotEmpty)
//                       Wrap(
//                         spacing: 8,
//                         children: (message["sources"] as List)
//                             .map<Widget>((source) => ElevatedButton.icon(
//                                   onPressed: () => openUrl(source["file_link"]),
//                                   icon: const Icon(Icons.link, color: Colors.white),
//                                   label: Text(source["title"], overflow: TextOverflow.ellipsis),
//                                   style: ElevatedButton.styleFrom(
//                                     backgroundColor: Colors.blue,
//                                     textStyle: const TextStyle(fontSize: 14),
//                                   ),
//                                 ))
//                             .toList(),
//                       ),
//                   ],
//                 );
//               },
//             ),
//           ),
//           Padding(
//             padding: const EdgeInsets.all(12),
//             child: Row(
//               children: [
//                 Expanded(
//                   child: TextField(
//                     controller: _queryController,
//                     decoration: const InputDecoration(
//                       hintText: "Ask something...",
//                       border: OutlineInputBorder(),
//                       contentPadding: EdgeInsets.symmetric(vertical: 12, horizontal: 12),
//                     ),
//                     onSubmitted: (_) => sendQuery(),
//                   ),
//                 ),
//                 const SizedBox(width: 8),
//                 IconButton(
//                   icon: isLoading
//                       ? const CircularProgressIndicator(color: Colors.blue)
//                       : const Icon(Icons.send),
//                   onPressed: isLoading ? null : sendQuery,
//                   color: isLoading ? Colors.grey : Colors.blue,
//                 ),
//               ],
//             ),
//           ),
//         ],
//       ),
//     );
//   }
// }

import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';
import 'package:flutter_markdown/flutter_markdown.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  ChatScreenState createState() => ChatScreenState();
}

class ChatScreenState extends State<ChatScreen> with AutomaticKeepAliveClientMixin {
  final TextEditingController _queryController = TextEditingController();
  final List<Map<String, dynamic>> messages = [];
  final ScrollController _scrollController = ScrollController();
  bool isLoading = false;

  @override
  bool get wantKeepAlive => true; // Keeps state alive for performance

  Future<void> sendQuery() async {
    String query = _queryController.text.trim();
    if (query.isEmpty || isLoading) return;

    setState(() {
      messages.insert(0, {"sender": "user", "message": query, "type": "text"});
      _queryController.clear();
      isLoading = true;
    });

    try {
      var response = await fetchResponse(query); // Removed `compute`

      if (response["status"] == 200) {
        setState(() {
          messages.insert(0, {
            "sender": "ai",
            "message": cleanText(response["message"]), // Encoding fix
            "sources": response["sources"] ?? []
          });
        });
      } else {
        showErrorMessage("Error fetching response.");
      }
    } catch (e) {
      showErrorMessage("An error occurred: $e");
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  Future<Map<String, dynamic>> fetchResponse(String query) async {
    final url = Uri.parse("https://commonly-golden-lionfish.ngrok-free.app/ask"); // Updated for emulator
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"query": query}),
    );

    if (response.statusCode == 200) {
      var jsonResponse = jsonDecode(response.body);
      return {
        "status": 200,
        "message": jsonResponse["response"] ?? "No response",
        "sources": jsonResponse["sources"] ?? []
      };
    }
    return {"status": response.statusCode, "message": "Error", "sources": []};
  }

  void showErrorMessage(String message) {
    setState(() {
      messages.insert(0, {"sender": "ai", "message": cleanText(message), "sources": []});
    });
  }

  void openUrl(String url) async {
    Uri uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Could not open the link: $url")),
      );
    }
  }

  /// **Fix for Unusual Characters**
  String cleanText(String text) {
    try {
      return utf8.decode(latin1.encode(text)); // Proper encoding fix
    } catch (e) {
      return text.replaceAll(RegExp(r'[^\x00-\x7F]'), ''); // Remove unusual characters as fallback
    }
  }

  @override
  Widget build(BuildContext context) {
    super.build(context); // Required for keeping state alive

    return Scaffold(
      appBar: AppBar(
        title: const Text("Vizzhy AI Agent", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
        centerTitle: true,
        backgroundColor: const Color.fromARGB(221, 91, 153, 240),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.separated(
              controller: _scrollController,
              padding: const EdgeInsets.all(12),
              reverse: true, // Automatically scrolls to the bottom
              itemCount: messages.length,
              separatorBuilder: (_, __) => const SizedBox(height: 10),
              itemBuilder: (context, index) {
                final message = messages[index];
                final isUser = message["sender"] == "user";

                return Column(
                  crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
                  children: [
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: isUser ? Colors.blue : Colors.grey[300],
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: message["sender"] == "ai"
                          ? MarkdownBody(
                              data: cleanText(message["message"]), // Fixed Encoding Issue
                              selectable: true,
                              styleSheet: MarkdownStyleSheet.fromTheme(Theme.of(context)).copyWith(
                                p: const TextStyle(fontSize: 16),
                              ),
                            )
                          : Text(
                              message["message"],
                              style: TextStyle(color: isUser ? Colors.white : Colors.black, fontSize: 16),
                            ),
                    ),
                    if (message.containsKey("sources") && message["sources"].isNotEmpty)
                      Wrap(
                        spacing: 8,
                        children: (message["sources"] as List)
                            .map<Widget>((source) => ElevatedButton.icon(
                                  onPressed: () => openUrl(source["file_link"]),
                                  icon: const Icon(Icons.link, color: Colors.white),
                                  label: Text(source["title"], overflow: TextOverflow.ellipsis),
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: Colors.blue,
                                    textStyle: const TextStyle(fontSize: 14),
                                  ),
                                ))
                            .toList(),
                      ),
                  ],
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _queryController,
                    decoration: const InputDecoration(
                      hintText: "Ask something...",
                      border: OutlineInputBorder(),
                      contentPadding: EdgeInsets.symmetric(vertical: 12, horizontal: 12),
                    ),
                    onSubmitted: (_) => sendQuery(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  icon: isLoading
                      ? const CircularProgressIndicator(color: Colors.blue)
                      : const Icon(Icons.send),
                  onPressed: isLoading ? null : sendQuery,
                  color: isLoading ? Colors.grey : Colors.blue,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

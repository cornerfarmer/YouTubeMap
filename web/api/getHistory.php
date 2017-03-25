<?php
    require("dbconnect.php");

    $result = $mysqli->query("SELECT video.identifier as video, channel.name as channel, (channel.id%10) as crawlerId, video.lastVisited as lastVisited FROM video LEFT JOIN channel ON video.channel_id = channel.id WHERE NOT video.lastVisited IS NULL ORDER BY lastVisited DESC LIMIT 50");

    if (!$result) {
        printf("Error: %s\n", $mysqli->error);
        exit();
    }

    echo json_encode($result->fetch_all(MYSQLI_ASSOC));
?>